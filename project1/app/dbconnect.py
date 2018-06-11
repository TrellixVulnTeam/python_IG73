import sqlite3

def connection():
    conn = sqlite3.connection(database='database.db')
    c = conn.cursor()

    return c, conn