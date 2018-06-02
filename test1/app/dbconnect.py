import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE = './test1.db'

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


