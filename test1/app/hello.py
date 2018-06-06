from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3

from wtforms import Form, StringField, BooleanField, PasswordField, DateTimeField, IntegerField, validators

from dbconnect import connection, close_connection


app = Flask(__name__)

 
@app.route("/")
def home():        
    return render_template('home.html', logged_in = session.get('logged_in'))
    
@app.route("/about/")
def about_us():
    return render_template('about.html', name="About Us")

@app.route("/about/<string:name>/")
def about(name):
    return render_template('about.html', name=name)


@app.route("/login/", methods =['GET', 'POST'] )
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            error = 'Invalid user'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/logout/")
def logout():
    session.clear()    
    return redirect(url_for('home'))


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=256)])
    email = StringField('Email', [validators.Length(min=6, max=30)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message = "Password must be match.")])
    confirm = PasswordField('Repeat Password')
    reg_date = DateTimeField('Registration Date',[])


@app.route("/registration/", methods =['GET', 'POST'] )
def registration():
    form = RegistrationForm(request.form)
    c, db = connection()
    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm = form.confirm.data
        c, db = connection()
        
        x = c.execute("SELECT * FROM registration WHERE username = (%s)", username)
        
        if int(x) > 0:
            flash("Username already exist, please choose another")
            return render_template('registration.html', form=form)        
        else:
            c.execute("INSERT INTO registration (username, email, password, confirm) VALUES (%s, %s, %s, %s)", (username, email, password, confirm) )
            db.commit()
           
            flash("Thanks for registration")
            c.close()
            db.close()

            session["logged_in"] = True
            session["username"] = request.form['username']
            return render_template('home.html')    
    return  render_template('registration.html',form=form)
    
    db.close()

    

if __name__ == "__main__":
    app.run(debug=True)