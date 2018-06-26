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
    username = StringField('Username :', [validators.length(min=1, max=256)])
    password = PasswordField('Password :', [validators.Required(), validators.EqualTo('password', message="Password must be match")] )
   
    
@app.route('/login/', methods=["POST","GET"])
def login():
    form = LoginForm()
    c, conn = connection()
    if request.method == "POST":
        
        c.execute("SELECT * FROM registration WHERE username= ? AND password= ?",(request.form['username'], request.form['password']))
        data = c.fetchone()

        if data:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash("You are now logged in")
            return redirect(url_for('home'))
        else:
            error = "Invalid user, Try again"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', form=form)
        c.close()
        conn.close()

class RegistrationForm(Form):
    username = StringField('Username :', [validators.Length(min=2, max=256)])
    age = StringField('Age :',[validators.Length(min=1, max=3)] )
    email = StringField('Email :', [validators.Length(min=6, max=30)])
    password = PasswordField('Password :', [validators.Required(), validators.EqualTo('password', message = "Password must be match.")])
    place = StringField('Place :', [validators.Length(min=1, max=256)])

@app.route('/registration/', methods=["POST", "GET"])
def registration():
    error = None
    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        username = form.username.data
        age = form.age.data
        email = form.email.data
        password = form.password.data
        place = form.place.data
        c, conn = connection()

        c.execute("SELECT * FROM registration WHERE username = ?", (username,))
        x = c.fetchone()

        if x:
            flash("Username already exist, Please choose another")
            return render_template('registration.html', form=form)
        else:
            c.execute("INSERT INTO registration (username, age, email, password, place) VALUES(?, ?, ?, ?, ?)", (username, age, email, password, place))
            conn.commit()
            flash("You are registered successfully")
            c.close()
            conn.close()

            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('home'))
    
    return render_template('registration.html', form=form)



@app.route('/logout/')
def logout():
    session.clear()
    flash("You are logged out now")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)