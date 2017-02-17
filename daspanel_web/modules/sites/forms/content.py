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
from wtforms import (TextField, SelectField)
from wtforms.validators import (Required, Email, URL, EqualTo, ValidationError,
                                StopValidation, Length, Optional)

_my_auth_types = [('NONE', 'None'), ('BASIC', 'HTTP Basic')]

# ============================
# Upload content from remote HTPP url form
# ============================
class NewUploadHttpForm(FlaskForm):
    """Create site form
    """
    version = SelectField(
        'Site Version',
        description='Site version where put the content',
        choices=[], default='ciyqaice400up7rp7piofia80',
        validators=[
            Required('Please select version'),
            Length(min=1, max=25)
            ]
    )

    auth_type = SelectField(
        'Authentication Type',
        description='Remote url authentication type',
        choices=_my_auth_types, default='NONE',
        validators=[
            Required('Please enter an auth type'),
            Length(min=1, max=15)
            ]
    )
    user = TextField(
        'User',
        description='User account, ignored if Auth Type = NONE',
        validators=[
            Optional(strip_whitespace=True),
            Length(min=1, max=255)
            ]
    )
    password = TextField(
        'Password',
        description='User password, ignored if Auth Type = NONE',
        validators=[
            Optional(strip_whitespace=True),
            Length(min=1, max=255)
            ]
    )
    url = TextField(
        'URL',
        description='URL of the ZIP file',
        validators=[
            Required('Please enter URL address'),
            URL(require_tld=True, message='Invalid URL'),
            Length(min=1, max=255)
            ]
    )
    directory = TextField(
        'Directory',
        description='Directory where put the content',
        default='/',
        validators=[
            Required('Please enter directory where put the content'),
            Length(min=1, max=255)
            ]
    )


