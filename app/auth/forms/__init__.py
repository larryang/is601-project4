""" auth forms """
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class login_form(FlaskForm): # pylint: disable=invalid-name
    """ login form """
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=6, max=35)
    ])
    submit = SubmitField()
