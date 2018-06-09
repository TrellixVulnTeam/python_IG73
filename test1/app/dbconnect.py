import sqlite3


datadir = 'C:\\sqlite3\\test1.db'
datafile = 'test1.db'
datadir = '../'
db = datadir+datafile


def connection():
    conn = sqlite3.connect(db)
         
    c = conn.cursor()

    return c, conn