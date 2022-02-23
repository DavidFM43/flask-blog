import sqlite3 

import click
from flask import current_app, g
from flask.cli import with_appcontext

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


def close_db():
    db = g.pop('db', None)

    if db is not None:
        # close connection to database
        db.close()