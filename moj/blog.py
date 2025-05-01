import logging

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from moj.auth import login_required
from moj.db import get_db


logger = logging.getLogger(__name__)

bp = Blueprint("blog", __name__)


def get_user_balance(id):
    balance = (
        get_db().execute("SELECT balance FROM user WHERE id = ?", (id,)).fetchone()
    )[0]

    logger.debug(f"User {id} balance: {balance}")

    return balance


def get_joke(id, check_author=True):
    joke = (
        get_db()
        .execute(
            "SELECT j.id, title, body, created, author_id, nickname"
            " FROM joke j JOIN user u ON j.author_id = u.id"
            " WHERE j.id = ?",
            (id,),
        )
        .fetchone()
    )

    if joke is None:
        logger.warning(f"Joke {id} not found.")
        abort(404, f"Joke id {id} doesn't exist.")

    if check_author and joke["author_id"] != g.user["id"]:
        logger.warning(f"Authorization failed for user {g.user['id']} on joke {id}.")
        abort(403)

    return joke


def get_community_joke(id, check_author=True):
    joke = (
        get_db()
        .execute(
            "SELECT j.id, title, body, created, author_id, nickname"
            " FROM joke j JOIN user u ON j.author_id = u.id"
            " WHERE j.id = ?",
            (id,),
        )
        .fetchone()
    )

    if joke is None:
        logger.warning(f"Joke {id} not found.")
        abort(404, f"Joke id {id} doesn't exist.")

    if check_author and joke["author_id"] == g.user["id"]:
        logger.warning(f"Authorization failed for user {g.user['id']} on joke {id}.")
        abort(403)

    return joke


@bp.route("/")
def index():
    db = get_db()
    community_jokes = db.execute(
        "SELECT j.id, title, body, created, author_id, nickname"
        " FROM joke j JOIN user u ON j.author_id = u.id"
        " ORDER BY created DESC",
    ).fetchall()
    logger.info(f"Community jokes: {community_jokes}")

    return render_template("blog/index.html", community_jokes=community_jokes)


@bp.route("/personal")
@login_required
def personal():
    if g.user["role"] == "moderator":
        return redirect(url_for("moderator.index"))

    db = get_db()
    user_jokes = db.execute(
        "SELECT j.id, title, body, created, author_id, nickname"
        " FROM joke j JOIN user u ON j.author_id = u.id"
        " WHERE u.id = ?"
        " ORDER BY created DESC",
        (g.user["id"],),
    ).fetchall()

    logger.info(f"User {g.user['id']} jokes: {user_jokes}")

    return render_template("blog/personal.html", user_jokes=user_jokes)


@bp.route("/community")
@login_required
def community():
    if g.user["role"] == "moderator":
        return redirect(url_for("moderator.index"))

    db = get_db()
    community_jokes = db.execute(
        "SELECT j.id, title, body, created, author_id, nickname"
        " FROM joke j JOIN user u ON j.author_id = u.id"
        " ORDER BY created DESC",
    ).fetchall()

    logger.info(f"Community jokes: {community_jokes}")

    return render_template("blog/community.html", community_jokes=community_jokes)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if g.user["role"] == "moderator":
        return redirect(url_for("moderator.index"))

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        balance = get_user_balance(g.user["id"]) + 1
        error = None

        if not title:
            error = "Title is required."
            logger.warning("Missing Title")

        if len(title.split(" ")) > 10:
            error = "Title must be no more than 10 words."
            logger.warning("Title is too long")

        if error is not None:
            flash(error)
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO joke (title, body, author_id) VALUES (?, ?, ?)",
                    (title, body, g.user["id"]),
                )
                db.execute(
                    "UPDATE user SET balance = ? WHERE id = ?", (balance, g.user["id"])
                )
                db.commit()
                logger.info(f"Joke created by user {g.user['id']}: {title}")
                return redirect(url_for("blog.personal"))
            except db.IntegrityError:
                error = "Joke was already created"
                logger.warning(f"Duplicate Joke: {title}")
            return redirect(url_for("blog.personal"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    if g.user["role"] == "moderator":
        return redirect(url_for("moderator.index"))

    joke = get_joke(id)
    if request.method == "POST":
        body = request.form["body"]
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE joke SET body = ? WHERE id = ?", (body, id))
            db.commit()
            logger.info(f"Joke {id} updated by user {g.user['id']}")
            return redirect(url_for("blog.personal"))

    return render_template("blog/update.html", joke=joke)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    if g.user["role"] == "moderator":
        return redirect(url_for("moderator.index"))

    db = get_db()
    db.execute("DELETE FROM joke WHERE id = ?", (id,))
    db.commit()
    logger.info(f"Joke {id} deleted by user {g.user['id']}")
    return redirect(url_for("blog.personal"))


@bp.route("/<int:id>/rate", methods=("GET", "POST"))
@login_required
def rate(id):
    if g.user["role"] == "moderator":
        return redirect(url_for("moderator.index"))

    joke = get_community_joke(id)

    if request.method == "POST":
        rating = request.form["rating"]
        error = None
        review = (
            get_db()
            .execute(
                "SELECT rating FROM review WHERE joke_id = ? AND user_id = ?",
                (id, g.user["id"]),
            )
            .fetchone()
        )

        if review is not None:
            error = "You have already rated this joke."
            logger.warning(f"User {g.user['id']} already rated joke {id}")

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO review (user_id, joke_id, rating) VALUES (?, ?, ?)",
                (g.user["id"], id, rating),
            )
            db.commit()
            logger.warning(f"User {g.user['id']} already rated joke {id}")
            return redirect(url_for("blog.personal"))

    return render_template("blog/rate.html", joke=joke)


@bp.route("/<int:id>/take", methods=("POST",))
@login_required
def take(id):
    joke = get_community_joke(id)
    balance = get_user_balance(g.user["id"]) - 1
    db = get_db()
    db.execute(
        "INSERT INTO joke (author_id, title, body) VALUES (?, ?, ?)",
        (g.user["id"], joke["title"], joke["body"]),
    )
    db.execute("UPDATE user SET balance = ? WHERE id = ?", (balance, g.user["id"]))
    db.commit()
    logger.info(f"User {g.user['id']} took joke {id}")

    if balance > 0:
        return redirect(url_for("blog.community"))
    else:
        return redirect(url_for("blog.personal"))
