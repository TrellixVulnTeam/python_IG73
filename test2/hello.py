from flask import Flask, render_template, flash

import sqlite3

from db import get_db, close_db
from form import LoginForm

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/login/")
def login():
    form = LoginForm
    return render_template('login.html', form=form, title="Login")

if (__name__ == "__main__"):
    app.run(debug=True)


