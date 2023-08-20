from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from market.models import User

class Registration(FlaskForm):
    def validate_username(self, username_to_change):
        user = User.query.filter_by(username=username_to_change.data).first()
        if(user):
            raise ValidationError("Username already exists! Please try a different one")
    
    def validate_email(self, email_to_change):
        email = User.query.filter_by(email=email_to_change.data).first()
        if email:
            raise ValidationError("Email already exists! Please try a different one")
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