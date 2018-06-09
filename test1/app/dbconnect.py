import sqlite3


datadir = 'C:/Users/developer/Desktop/test1.db'
datafile = 'test1.DB'
datadir = '../'
db = datadir+datafile


def connection():
    conn = sqlite3.connect(db)
         
    c = conn.cursor()

    return c, conn