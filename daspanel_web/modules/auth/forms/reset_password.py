import urlparse

from flask import g
from flask_wtf import FlaskForm
from wtforms import (TextField, PasswordField, BooleanField, TextAreaField,
                     FileField)
from wtforms.validators import (Required, Email, URL, EqualTo, ValidationError,
                                StopValidation)
from wtforms.widgets import PasswordInput, CheckboxInput
from ..models import User
from daspanel_web.lib.util import verify_password_hash


# ============================
# Auth forms
# ============================
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            Required('Please choose a password'),
            EqualTo('password_confirm', message='Passwords must match')
            ])

    password_confirm = PasswordField(
        'Confirm Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            Required('Please confirm your password')
            ])

