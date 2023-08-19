from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo

class Registration(FlaskForm):
    username = StringField("Username: ",
        validators=[
            Length(min=3, max=50),
            DataRequired()
        ])
    email = StringField("Email: ",
        validators=[
            Email(),
            DataRequired()
        ])
    password = PasswordField("Password: ",
        validators=[
            Length(min=6),
            DataRequired()
        ])
    confirm_password = PasswordField("Confirm password: ",
        validators=[
            EqualTo('password', message="Password doesn't match")
        ])
    submit = SubmitField("Create Account")