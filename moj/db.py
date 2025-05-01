import logging
import sqlite3
from datetime import datetime

import click
from flask import Flask, current_app, g

from werkzeug.security import generate_password_hash


logger = logging.getLogger(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        logger.debug("Database connection established")

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
        logger.debug("Database connection closed")


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
        logger.info("Database schema initialized successfully")


def add_moderator():
    db = get_db()

    db.execute(
        "INSERT INTO user (email, nickname, password, balance, role) VALUES"
        "(?, ?, ?, ?, ?)",
        (
            "testadmin@gmail.com",
            "testadmin",
            generate_password_hash("Test123"),
            0,
            "moderator",
        ),
    )
    db.commit()
    logger.info("testadmin moderator added")


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("add-moderator")
def add_moderator_command():
    """Add a moderator account to database"""
    add_moderator()
    click.echo("Moderator added")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_moderator_command)
