from flask import Flask
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators, ValidationError

class LoginForm(Form):
    username = StringField('Username', [validators.Required("Please enter your name")])
    password = PasswordField('Password', [validators.Required("Enter password")])
    submit = SubmitField('Login')