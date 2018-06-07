import sqlite3

db = 'C:/Users/developer/Desktop/test1.db'

def connection():
    conn = sqlite3.connect(database="test1")
         
    c = conn.cursor()

    return c, conn