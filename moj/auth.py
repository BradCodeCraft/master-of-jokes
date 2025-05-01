import functools
import logging


from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from moj.db import get_db

import re

logger = logging.getLogger(__name__)


bp = Blueprint("auth", __name__, url_prefix="/auth")


def validate_email(email):
    """
    Checks if the given string is a valid email address using regex.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email):
        return True
    else:
        return False


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"].lower()
        nickname = request.form["nickname"].lower()
        password = request.form["password"]
        db = get_db()
        error = None

        if not email:
            error = "Email is required."
            logger.warning("Email is missing")
        elif not validate_email(email):
            error = "Invalid email address"
            logger.warning("Invalid email address")
        elif not nickname:
            error = "Nickname is required"
            logger.warning("Nickname is missing")
        elif not password:
            error = "Password is required."
            logger.warning("Password is missing")

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, nickname, password, balance, role) VALUES (?, ?, ?, ?, ?)",
                    (email, nickname, generate_password_hash(password), 0, "user"),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {nickname} is already registered."
                logger.warning(f"User {nickname} is already registered")
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        nickname = request.form["nickname"].lower()
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE email = ? OR nickname = ?",
            (nickname, nickname),
        ).fetchone()

        if user is None:
            error = "Incorrect nickname or email."
            logger.warning("Authentication Failed: Incorrect nickname or email")
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
            logger.warning("Authentication Failed: Incorrect password")

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            logger.info("Authentication Successful")
            return (
                redirect(url_for("blog.create"))
                if user["role"] == "user"
                else redirect(url_for("moderator.index"))
            )

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            logger.warning("User not logged in")
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def moderator_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            logger.warning("User not logged in")
            return redirect(url_for("auth.login"))
        if g.user["role"] != "moderator":
            logger.warning("User is not a moderator")
            return redirect(url_for("blog.index"))

        return view(**kwargs)

    return wrapped_view
