from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Create Password:', validators=[DataRequired(), Length(min=3, max=40), EqualTo('confirm', message='The passwords must match.')])
    confirm = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password', message='The passwords must match.')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()