from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class Registration(FlaskForm):
    username = StringField("Username: ")
    email = StringField("Email: ")
    password = PasswordField("Password: ")
    confirm_password = PasswordField("Confirm password: ")
    submit = SubmitField("Create Account")