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
class LoginForm(FlaskForm):
    """Sign in form
    """
    email = TextField(
        'Email address',
        validators=[
            Required('Please enter your email address'),
            Email()
            ])

    password = PasswordField(
        'Password',
        widget=PasswordInput(hide_value=False),
        validators=[
            Required('Please enter your password')
            ])

    remember_me = BooleanField(
        'Remember me',
        widget=CheckboxInput(),
        default=True)

    def validate_password(form, field):
        """Verify password
        """
        if not form.email.data:
            raise StopValidation()
        
        # get user and verify password
        u = User.query.filter(User.email == form.email.data).first()
        if not u or not verify_password_hash(field.data, u.password):
            raise ValidationError('Email and password must match')

