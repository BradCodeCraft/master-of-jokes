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

from moj.auth import moderator_required
from moj.db import get_db

bp = Blueprint("moderator", __name__)


def get_all_users():
    users = get_db().execute("SELECT * FROM user WHERE role LIKE 'user'").fetchall()

    return users


def get_all_moderators():
    moderators = (
        get_db().execute("SELECT * FROM user WHERE role LIKE 'moderator'").fetchall()
    )

    return moderators


def get_user_by_id(id):
    user = get_db().execute("SELECT * FROM user WHERE id == ?", (id,)).fetchone()

    return user


def get_all_jokes():
    jokes = get_db().execute("SELECT * FROM joke")

    return jokes


def get_joke(id):
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
        abort(404, f"Joke id {id} doesn't exist.")

    return joke


@bp.route("/moderator")
@moderator_required
def index():
    return render_template("moderator/index.html")


@bp.route("/moderator/users")
@moderator_required
def get_users():
    users = get_all_users()

    return render_template("moderator/users.html", users=users)


@bp.route("/moderator/users/<int:id>/update", methods=("GET", "POST"))
@moderator_required
def update_user_balance(id):
    user = get_user_by_id(id)

    if request.method == "POST":
        balance = request.form["user_balance"]
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("UPDATE user SET balance = ? WHERE id = ?", (balance, id))
            db.commit()
            return redirect(url_for("moderator.get_users"))

    return render_template("moderator/update-user-balance.html", user=user)


@bp.route("/moderator/<int:id>/make-moderator", methods=("POST",))
@moderator_required
def make_moderator(id):
    db = get_db()
    db.execute("UPDATE user SET role = 'moderator' WHERE id = ?", (id,))
    db.commit()

    return redirect(url_for("moderator.index"))


@bp.route("/moderator/<int:id>/remove-moderator", methods=("POST",))
@moderator_required
def remove_moderator(id):
    db = get_db()
    db.execute("UPDATE user SET role = 'user' WHERE id = ?", (id,))
    db.commit()

    if g.user["role"] != "moderator":
        return redirect(url_for("blog.create"))

    return redirect(url_for("moderator.index"))


@bp.route("/moderator/moderators")
@moderator_required
def get_moderators():
    moderators = get_all_moderators()

    return render_template("moderator/moderators.html", moderators=moderators)


@bp.route("/moderator/jokes")
@moderator_required
def jokes():
    jokes = get_all_jokes()

    return render_template("moderator/jokes.html", jokes=jokes)


@bp.route("/moderator/<int:id>/update", methods=("GET", "POST"))
@moderator_required
def update_joke(id):
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
            return redirect(url_for("moderator.jokes"))

    return render_template("moderator/update-joke.html", joke=joke)


@bp.route("/moderator/<int:id>/delete", methods=("POST",))
@moderator_required
def delete_joke(id):
    db = get_db()
    db.execute("DELETE FROM joke WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("moderator.jokes"))
