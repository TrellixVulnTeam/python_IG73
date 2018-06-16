from flask import Flask, render_template, session, redirect, request, flash, url_for
import sqlite3

from wtforms import Form, StringField, PasswordField, IntegerField, validators

from dbconnect import connection

app = Flask(__name__)
app.secret_key = "my first secret key"

@app.route('/')
def home():
    return render_template('home.html')

class LoginForm():
    username = StringField('Username', [validators.length(min=1, max=256)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password', message="Password must be match")] )
   
    
@app.route('/login/', methods=['POST','GET'])
def login():
    form = LoginForm()
    c,conn = connection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        c.execute("SELECT * FROM user WHERE username= ? AND password= ?",(username,password))
        data = c.fetchone()[2]

        if data:
            session['logged_in'] = True
            session['username'] = username
            flash("You are now logged in")
            return redirect(url_for('home'))
        else:
            flash("You are not autorise to login")
            return render_template('login.html')
    else:
        return render_template('login.html')
        c.close()
        conn.close()

class RegistrationForm():
    username = StringField('Username', [validators.Length(min=4, max=256)])
    age = StringField('Age',[validators.Length(min=1, max=3)] )
    email = StringField('Email', [validators.Length(min=6, max=30)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password', message = "Password must be match.")])
    place = StringField('Place', [validators.Length(min=1, max=256)])

@app.route('/regisration/', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    c, conn = connection()
    if request.method == 'POST' and form.validate():
        username = request.form.data
        age = request.form.data
        email = request.form.data
        password = request.form.data
        place = request.form.data

        c.execute("SELECT * FROM registration WHERE username= ?",username)
        x = c.fetchone()

        if x:
            flash("Username already exist, Please choose another")
            return render_template('registration.html')
        else:
            c.execute("INSERT INTO registration username= ?, age= ?, email= ?, password= ?, place= ?", (username, age, email, password, place))
            c.commit()
            flash("You are registered successfully")
            c.close()
            conn.close()

            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('home'))
    
    return render_template('registration.html')



@app.route('/logout/')
def logout():
    session.clear()
    flash("You are logged out now")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)