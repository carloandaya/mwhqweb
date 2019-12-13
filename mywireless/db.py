import pyodbc

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pyodbc.connect(
            current_app.config['DW_DATABASE']
        )
    return g.db


def get_db_raw():
    if 'db_raw' not in g:
        g.db_raw = pyodbc.connect(
            current_app.config['RAW_DATABASE']
        )
    return g.db_raw


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def close_db_raw(e=None):
    db_raw = g.pop('db_raw', None)

    if db_raw is not None:
        db_raw.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        sqlScript = f.read().decode('utf8')
        for statement in sqlScript.split(';'):
            db.execute(statement)
            db.commit()

    db_raw = get_db_raw()

    with current_app.open_resource('schema_raw.sql') as f:
        sqlScript = f.read().decode('utf8')
        for statement in sqlScript.split(';'):
            db_raw.execute(statement)
            db_raw.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.teardown_appcontext(close_db_raw)
