import pyodbc

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pyodbc.connect(
            current_app.config['DATABASE']
        )
        # g.db.row_factory = pyodbc.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        sqlScript = f.read().decode('utf8')
        for statement in sqlScript.split(';'):
            db.execute(statement)
            db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
