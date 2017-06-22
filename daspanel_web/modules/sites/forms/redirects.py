#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Daspanel CP sites module
~~~~~~~~~~~~~~~~~~~~~~~~

Form for Daspanel sites module.

:copyright: (c) 2017 by Abner G Jacobsen
:licence: GNU General Public License v3, see LICENSE for more details.
"""
import urlparse
from flask import g
from flask_wtf import FlaskForm
from wtforms import (TextField, SelectField, BooleanField)
from wtforms.validators import (Required, Email, URL, EqualTo, ValidationError,
                                StopValidation, Length, Optional, Regexp)
#from wtforms.widgets import PasswordInput, CheckboxInput
#from daspanel_web.lib.util import verify_password_hash

_my_confirmation = [('no', 'NO'), ('yes', 'YES')]
_ssl_type = [('self', 'Self-signed'), ('auto', 'AutoSSL (Lets Encrypt)'), ('letsencrypt', 'Lets Encrypt')]

# ============================
# Confirmation form
# ============================
class DeleteRedirectForm(FlaskForm):
    """Confirm operation form
    """
    confirm = SelectField(
        'You really want to delete this site redirect ?',
        description='You really want to delete this site redirect ?',
        choices=_my_confirmation, default='no',
        validators=[
            Required('Please confirm site redirect delete'),
            Length(min=1, max=64)
            ]
    )

    def validate_confirm(form, field):
        """Check if is confirmed
        """
        if not field.data =='yes':
            raise ValidationError('You must select YES to confirm the operation.')

# ============================
# New site redirect form
# ============================
class NewRedirectForm(FlaskForm):
    """Create site redirect form
    """
    version = SelectField(
        'Site Version',
        description='Site version where redirect the URL',
        choices=[], default='ciyqaice400up7rp7piofia80',
        validators=[
            Required('Please select version'),
            Length(min=25, max=25)
        ]
    )
    domain = TextField(
        'Domain',
        description='Redirect domain',
        validators=[
            Required('Please enter an redirect domain'),
            Length(min=1, max=255),
            Regexp(
                '(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', 
                message='Invalid domain')
        ]
    )
    hosturl = TextField(
        'Host',
        description='Host',
        validators=[
            Required('Please enter domain host, like www, www2, etc'),
            Length(min=1, max=255),
            Regexp('^[a-zA-Z0-9-]+$', 
                message='Invalid host. Only letters and numbers allowed')
        ]
    )
    ssl = SelectField(
        'SSL type',
        description='What type of SSL certificate do you want to use?',
        choices=_ssl_type, default='self',
        validators=[
            Required('Please select your ssl certificate type'),
            Length(min=1, max=64)
        ]
    )
    #ssl = BooleanField(
    #    'With SSL',
    #    description='Redirect have SSL ?',
    #    default=True
    #)
    sslcert = TextField(
        'SSL certificate file name',
        description='Option SSL certificate file name',
        validators=[
            Optional(strip_whitespace=True),
            Length(min=1, max=255)
            ]
    )
    sslkey = TextField(
        'SSL certificate key file name',
        description='Option SSL certificate key file name',
        validators=[
            Optional(strip_whitespace=True),
            Length(min=1, max=255)
            ]
    )


class EditRedirectForm(FlaskForm):
    """Edit site redirect form
    """
    version = SelectField(
        'Site Version',
        description='Site version where redirect the URL',
        choices=[], default='ciyqaice400up7rp7piofia80',
        validators=[
            Required('Please select version'),
            Length(min=25, max=25)
        ]
    )
    domain = TextField(
        'Domain',
        description='Redirect domain',
        validators=[
            Required('Please enter an redirect domain'),
            Length(min=1, max=255),
            Regexp(
                '(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', 
                message='Invalid domain')
        ]
    )
    hosturl = TextField(
        'Host',
        description='Host',
        validators=[
            Required('Please enter domain host, like www, www2, etc'),
            Length(min=1, max=255),
            Regexp('^[a-zA-Z0-9-]+$', 
                message='Invalid host. Only letters and numbers allowed')
        ]
    )
    ssl = SelectField(
        'SSL type',
        description='What type of SSL certificate do you want to use?',
        choices=_ssl_type, default='self',
        validators=[
            Required('Please select your ssl certificate type'),
            Length(min=1, max=64)
        ]
    )
    #ssl = BooleanField(
    #    'With SSL',
    #    description='Redirect have SSL ?',
    #    default=True
    #)
    sslcert = TextField(
        'SSL certificate file name',
        description='Option SSL certificate file name',
        validators=[
            Optional(strip_whitespace=True),
            Length(min=1, max=255)
            ]
    )
    sslkey = TextField(
        'SSL certificate key file name',
        description='Option SSL certificate key file name',
        validators=[
            Optional(strip_whitespace=True),
            Length(min=1, max=255)
            ]
    )


