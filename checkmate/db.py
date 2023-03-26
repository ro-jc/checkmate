from pymongo import MongoClient
import click

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        client = MongoClient()["checkmate"]
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def reset_db():
    MongoClient().drop_database()
    get_db()  # reset g.db


@click.command("init-db")
@with_appcontext
def reset_db_command():
    reset_db()
    click.echo("Database has been reset")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(reset_db_command)
