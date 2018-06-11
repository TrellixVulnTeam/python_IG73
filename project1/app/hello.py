from flask import Flask, render_template, session, redirect, request, flash, url_for
import sqlite3

from wtforms import Form, StringField, PasswordField, IntegerField, validators

from dbconnect import connection

app = Flask(__name__)
app.secret_key = "my first secret key"

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/', methods=['POST','GET'])
def new_user():
    c, conn = connection()
    if request.method == 'POST':
        c.execute("SELECT * FROM user WHERE username=(?)",[username])

    
    c.execute("SELECT * FROM user")
    rv = c.fetchall()
    return str(rv)



if __name__ == "__main__":
    app.run(debug=True)