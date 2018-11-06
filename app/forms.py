from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email address"})
    password_0 = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    password_1 = PasswordField('Password again', 
            validators=[DataRequired(), EqualTo('password_0')], render_kw={"placeholder": "Password again"})
    submit = SubmitField('Submit')

