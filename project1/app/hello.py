from flask import Flask, render_template, session, redirect, request, flash, url_for
import sqlite3

from wtforms import Form, StringField, PasswordField, IntegerField, validators

from dbconnect import connection

app = Flask(__name__)
app.secret_key = "my first secret key"

@app.route('/')
def home():
    return render_template('home.html')

def LoginForm():
    username = StringField('Username', [validators.length(min=1, max=256)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password', message="Password must be match")] )
   
    
@app.route('/login/', methods=['POST','GET'])
def login():
    form = LoginForm()
    c,conn = connection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = "SELECT * FROM user WHERE username= ? AND password= ?",([username],[password])
        c.execute(data)
        if int(data=0):
            flash("You are not authorise to login")
        else:
            flash("You are already login")
    else:
        if int(data=0):

    c.close()
    conn.close()

@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out now")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)