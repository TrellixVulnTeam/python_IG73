import sqlite3

db = 'C:/Users/developer/Desktop/test1.db'


def connection():
    conn = db.cursor()
    if db is None:
       sqlite3.connect(db)
    return conn, db 

def close_connection():
    if db is not None:
        db.close()


