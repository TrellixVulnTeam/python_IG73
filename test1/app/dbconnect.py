import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE = '/test1.db'

def connection():
    db = getattr(g,'_test1', None)
    if db is None:
        db = g._test1 = sqlite3.connect(DATABASE)
    
    c = db.cursor()

    return c, db 

def close_connection():
    db = getattr(g,'_test1', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('table1.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
