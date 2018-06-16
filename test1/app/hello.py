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

def login_required():
    if 'logged_in' in session:
        flash("You already log in")
    else:
        flash("You need to login first")
        return redirect(url_for('login'))

@app.route("/logout/")
def logout():
    session.clear() 
    flash("You have been logged out")   
    return redirect(url_for('home'))


@app.route("/login/", methods =['GET', 'POST'] )
def login():
    error= 'None'
    c, conn = connection()
    if request.method == 'POST':
        data = c.execute("SELECT * FROM `user` WHERE `username` = ? AND `password` = ?", (request.form['username'], request.form['password']))
        data = c.fetchone()
        if data:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash("You are now logged in")
            return redirect(url_for('home'))
        else:
            error = "Invalid User"
    return render_template('login.html', error=error)



class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=256)])
    age = StringField('Age',[validators.Length(min=1, max=3)] )
    email = StringField('Email', [validators.Length(min=6, max=30)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('password', message = "Password must be match.")])
    place = StringField('Place', [validators.Length(min=1, max=256)])
    
@app.route("/registration/", methods =['GET', 'POST'] )
def registration():
    form = RegistrationForm(request.form)
    c, conn = connection()
    if request.method == "POST" and form.validate():
        username = form.username.data
                
        c.execute("SELECT * FROM registration WHERE username = (?)", [username])
        x= c.fetchone()
        if x:
            flash("Username already exist, please choose another")
            return render_template('registration.html', form=form)        
        else:
            username = form.username.data
            age = form.age.data
            email = form.email.data
            password = form.password.data
            place = form.place.data
            c, conn = connection()

            c.execute("INSERT INTO registration (username, age, email, password, place) VALUES (?, ?, ?, ?, ?)))", ([username], [age], [email], password, place) )
            conn.commit()
           
            flash("Thanks for registration")
            conn.close()
            c.close()

            session["logged_in"] = True
            session["username"] = request.form['username']
            return render_template('home.html') 

    return  render_template('registration.html',form=form)
    
    db.close()

    

if __name__ == "__main__":
    app.run(debug=True)