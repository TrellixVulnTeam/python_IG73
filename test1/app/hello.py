from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3

from wtforms import Form, StringField, BooleanField, PasswordField, DateTimeField, IntegerField, validators

from dbconnect import connection


app = Flask(__name__)
app.secret_key = 'my best secret key'

 
@app.route("/")
def home():        
    return render_template('home.html', logged_in = session.get('logged_in'))
    
@app.route("/about/")
def about_us():
    return render_template('about.html', name="About Us")

@app.route("/about/<string:name>/")
def about(name):
    return render_template('about.html', name=name)

class LoginForm():
    username = StringField('Username', [validators.length(min=1, max=256)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password', message = "Password must be match.")])

@app.route('/login/', methods =["GET", "POST"] )
def login():
    error= 'None'
    form = LoginForm()
    c,conn = connection()
    if request.method == "POST":
        c.execute("SELECT * FROM user WHERE username= ? AND password= ?",(request.form['username'], request.form['password']))
        data = c.fetchone()

        if data:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash("You are now logged in")
            return redirect(url_for('home'))
        else:
            error = "Invalid User, Try again"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', form=form)
        conn.close()
        c.close()



class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=256)])
    age = StringField('Age',[validators.Length(min=1, max=3)] )
    email = StringField('Email', [validators.Length(min=6, max=30)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password', message = "Password must be match.")])
    
@app.route('/registration/', methods =["GET", "POST"])
def registration():
    error = None
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        age = form.age.data
        email = form.email.data
        password = form.password.data
        c,conn = connection()
                
        c.execute("SELECT * FROM registration WHERE username = (?)", (username,))
        x = c.fetchone()
        if x:
            flash("Username already exist, please choose another")
            return render_template('registration.html', form=form)        
        else:
            c.execute("INSERT INTO registration (username, age, email, password) VALUES(?, ?, ?, ?)", (username, age, email, password))
            conn.commit()

            flash("Thanks for registration")
            c.close()
            conn.close()
            session['logged_in'] = True
            session["username"] = request.form['username']
            return redirect(url_for('home'))
    else:
        return  render_template('registration.html',form=form)

@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out")   
    return redirect(url_for('home'))

    
if __name__ == "__main__":
    app.run(debug=True)