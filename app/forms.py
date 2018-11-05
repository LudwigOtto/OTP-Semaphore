from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password_0 = PasswordField('Password', validators=[DataRequired()])
    password_1 = PasswordField(
        'Password again', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
