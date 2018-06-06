from flask import Flask, g
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("localhost","root","database")
        g.db.row_factory = sql.Row
        c = g.db.cursor()
    return c, g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db_close()