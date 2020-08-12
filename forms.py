from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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


class LoginForm(FlaskForm):
    # Only validates input if i) not empty, ii) correct address email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')