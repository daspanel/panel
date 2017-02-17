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
class CreateAccountForm(FlaskForm):
    """Create account form
    """
    email = TextField(
        'Email address',
        validators=[
            Required('Please enter an email address'),
            Email()
            ])

    password = PasswordField(
        'Password',
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

    newsletter = BooleanField(
        'Please send me product updates',
        widget=CheckboxInput(),
        default=True
        )

    def validate_email(form, field):
        """Check if email already exists
        """
        u = User.query.filter(User.email == field.data).first()
        if u != None:
            raise ValidationError('Did your forget your password?')

