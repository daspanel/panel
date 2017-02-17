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
class ForgotPasswordForm(FlaskForm):
    email = TextField(
        'Email address',
        validators=[
            Required('Please enter an email address'),
            Email()
            ])

    def validate_email(form, field):
        """Check if email exists
        """
        u = User.query.filter(User.email == field.data).first()
        if u == None:
            raise ValidationError('Sorry, %s is not registered' % field.data)

