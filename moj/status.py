from flask import (
    Blueprint,
    jsonify,
)

from moj.db import get_db

bp = Blueprint("status", __name__)


def get_all_users():
    users = get_db().execute("SELECT * FROM user").fetchall()

    return users


def get_all_jokes():
    jokes = get_db().execute("SELECT * FROM joke").fetchall()

    return jokes


@bp.route("/api/moj/users")
def users_api():
    users = get_all_users()
    users = [tuple(user) for user in users]

    response = jsonify(users)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@bp.route("/api/moj/jokes")
def jokes_api():
    jokes = get_all_jokes()
    jokes = [tuple(joke) for joke in jokes]

    response = jsonify(jokes)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response
