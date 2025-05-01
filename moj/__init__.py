import os
import logging
import sys
import functools
from flask import Flask, request, session
from flask_cors import CORS

# this is all logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

consolestream = logging.StreamHandler(sys.stdout)
consolestream.setLevel(logging.WARNING)

logfile = logging.FileHandler("moj.log")
logfile.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s [%(module)s]: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

consolestream.setFormatter(formatter)
logfile.setFormatter(formatter)

logger.addHandler(consolestream)
logger.addHandler(logfile)


def set_debug_mode(enabled):
    level = logging.DEBUG if enabled else logging.INFO
    logfile.setLevel(level)
    logger.info(f"Log file level set to {'DEBUG' if enabled else 'INFO'}")


def log_function_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering: {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"Exiting: {func.__name__} with result: {result}")
        return result

    return wrapper


def create_app(test_config=None):
    # create and configure the app
    logger.info("Starting moj server")

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "moj.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    if app.debug:
        set_debug_mode(True)
    else:
        set_debug_mode(False)

    logger.info(f"Config loaded: {app.config}")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    try:
        db.init_app(app)
        logger.info("Database initialized")
    except Exception:
        logger.critical("Unable to initialize database")
        raise

    from . import auth

    app.register_blueprint(auth.bp)
    logger.info("Auth blueprint registered")

    from . import blog

    app.register_blueprint(blog.bp)
    logger.info("Blog blueprint registered")
    app.add_url_rule("/", endpoint="index")

    from . import moderator

    app.register_blueprint(moderator.bp)
    logger.info("Moderator blueprint registered")

    from . import status

    app.register_blueprint(status.bp)
    logger.info("Status blueprint registered")

    def log_session():
        sid = session.get("user_id", "anonymous")
        logger.debug(
            f"Processing request {request.method} {request.path} | Session ID: {sid}"
        )

    def log_response(response):
        logger.info(
            f"{request.path} from {request.endpoint}, returned {response.status_code}"
        )
        if response.status_code != 200:
            logger.warning(f"{response.status_code} for {request.path}")
        return response

    def log_exception(e):
        code = getattr(e, "code", 500)
        if code >= 500:
            logger.error("Unexpected exception (500+):", exc_info=e)
        return "An error occurred", code

    app.before_request(log_session)
    app.after_request(log_response)
    app.register_error_handler(Exception, log_exception)

    import atexit

    def log_shutdown():
        logger.info("Shutting down moj server")

    atexit.register(log_shutdown)

    @log_function_calls
    def get_joke_rating(joke_id):
        joke_ratings = (
            db.get_db()
            .execute(
                "SELECT rating FROM review WHERE joke_id = ?",
                (joke_id,),
            )
            .fetchall()
        )
        logger.debug(f"Query returned: {joke_ratings}")

        sum = count = 0

        for joke_rating in joke_ratings:
            sum += joke_rating[0]
            count += 1

        return sum / count if count >= 1 else 0

    @log_function_calls
    def has_rated(user_id, joke_id):
        joke_review = (
            db.get_db()
            .execute(
                "SELECT rating FROM review WHERE joke_id = ? AND user_id = ?",
                (joke_id, user_id),
            )
            .fetchone()
        )
        logger.debug(f"Query returned: {joke_review}")

        return joke_review is not None

    @log_function_calls
    def has_joke(user_id, joke_title):
        user_joke = (
            db.get_db()
            .execute(
                "SELECT j.id FROM joke j JOIN user u ON j.author_id = u.id"
                " WHERE author_id = ? AND title = ? ORDER BY created DESC",
                (user_id, joke_title),
            )
            .fetchone()
        )
        logger.debug(f"Query returned: {user_joke}")

        return user_joke is not None

    @log_function_calls
    def can_remove_moderators(moderators):
        logger.debug(f"Function returned: {len(moderators) > 1}")
        return len(moderators) > 1

    app.jinja_env.globals.update(get_joke_rating=get_joke_rating)
    app.jinja_env.globals.update(has_rated=has_rated)
    app.jinja_env.globals.update(has_joke=has_joke)
    app.jinja_env.globals.update(can_remove_moderators=can_remove_moderators)

    return app
