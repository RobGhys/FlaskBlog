from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    # Only validates input from user if i) some data are present, and ii) length is respected
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # Only validates input if i) not empty, ii) correct address email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # Should not be empty
    password = PasswordField('Password',
                             validators=[DataRequired()])
    # Should match 'password' and not be empty
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        # Returns the user name if it exists, or returns None if it doesn't exist
        user = User.query.filter_by(username=username.data).first()
        # Raise the error if the use is None
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')


    def validate_email(self, email):
        # Returns the user name if it exists, or returns None if it doesn't exist
        user = User.query.filter_by(email=email.data).first()
        # Raise the error if the use is None
        if user:
            raise ValidationError('Email already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    # Use email as the login form instead of user name
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Using secure cookie, enables the user logs to be remembered
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')