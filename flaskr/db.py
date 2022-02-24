import sqlite3 

import click
from flask import current_app, g
from flask.cli import with_appcontext

# TODO: Maybe create a Database class to encapsulate this functions.
# Question: Is it better to put functions inside a module or inside a class?


# Question: Does init_db get used without the command?
def init_db():
    db = get_db()
    # executes the .sql script for creating empty tables
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# create a command line command named 'init-db'
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Registers the database methods with the application instance"""

    # call close_db after returning a response to a request
    app.teardown_appcontext(close_db)
    # adds new command that can be called with Flask
    app.cli.add_command(init_db_command)


def get_db():
    # g is an object that handles requests information
    if 'db' not in g:
        # connect to database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], 
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # db returns rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        # close connection to database
        db.close()
