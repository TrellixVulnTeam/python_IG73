from flask import Flask, render_template, session, redirect, request, flash, url_for
import sqlite3

from wtforms import Form, StringField, PasswordField, IntegerField, validators

from dbconnect import connection

app = Flask(__name__)
app.secret_key = "my first secret key"

@app.route('/')
def home():
    return render_template('home.html')

class LoginForm(Form):
    

@app.route('/user/', methods=['POST','GET'])
def user_login():
    c, conn = connection()
    if request.method == 'POST':
        c.execute("SELECT * FROM user WHERE username=(?)",[username])

    
    c.execute("SELECT * FROM user")
    rv = c.fetchall()
    return render_template("user.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out now")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)