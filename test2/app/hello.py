from flask import Flask, render_template, redirect, url_for, request, session, flash

from wtforms import Form, StringField, BooleanField, PasswordField, DateTimeField, IntegerField, validators
from flask_wtf import Form
from flask_login import LoginManager, login_required
import sqlite3

from db import get_db, close_db
from form import LoginForm

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm
    if request.method == 'POST' and form.validate() == 'False':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            flash ('Invalid user')
        else:
            session['logged_in'] = 'True'
            session['username'] = request.form['username']
            return render_template('home.html')
    else:
        return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

       
   

if (__name__ == "__main__"):
    app.run(debug=True)


