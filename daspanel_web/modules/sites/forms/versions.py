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
                                StopValidation, Length)
#from wtforms.widgets import PasswordInput, CheckboxInput
#from daspanel_web.lib.util import verify_password_hash

_my_types = [('generic', 'Generic PHP site'), ('grav', 'Grav'), ('wordpress', 'Wordpress')]
_my_runtimes = [('php70', 'PHP 7.0'), ('php56', 'PHP 5.6')]
_my_confirmation = [('no', 'NO'), ('yes', 'YES')]

# ============================
# Confirmation form
# ============================
class DeleteVersionForm(FlaskForm):
    """Confirm operation form
    """
    confirm = SelectField(
        'You really want to delete this site version ?',
        description='You really want to delete this site version ?',
        choices=_my_confirmation, default='no',
        validators=[
            Required('Please confirm site version delete'),
            Length(min=1, max=64)
            ]
    )

    def validate_confirm(form, field):
        """Check if is confirmed
        """
        if not field.data =='yes':
            raise ValidationError('You must select YES to confirm the operation.')

# ============================
# New site form
# ============================
class NewVersionForm(FlaskForm):
    """Create site version form
    """
    description = TextField(
        'Description',
        description='Version Description',
        validators=[
            Required('Please enter an version description'),
            Length(min=1, max=255)
        ]
    )
    tag = TextField(
        'Tag',
        description='Version Tag',
        validators=[
            Required('Please enter an version tag'),
            Length(min=1, max=255)
        ]
    )
    sitetype = SelectField(
        'Type',
        description='Site Type',
        choices=_my_types, default='generic',
        validators=[
            Required('Please enter an site type'),
            Length(min=1, max=64)
            ]
    )
    runtime = SelectField(
        'Engine',
        description='Site Engine',
        choices=_my_runtimes, default='php70',
        validators=[
            Required('Please enter an site engine'),
            Length(min=1, max=64)
            ]
    )


class EditVersionForm(FlaskForm):
    """Edit site version form
    """
    description = TextField(
        'Description',
        description='Version Description',
        validators=[
            Required('Please enter an version description'),
            Length(min=1, max=255)
        ]
    )
    tag = TextField(
        'Tag',
        description='Version Tag',
        validators=[
            Required('Please enter an version tag'),
            Length(min=1, max=255)
        ]
    )
    sitetype = SelectField(
        'Type',
        description='Site Type',
        choices=_my_types, default='generic',
        validators=[
            Required('Please enter an site type'),
            Length(min=1, max=64)
            ]
    )
    runtime = SelectField(
        'Engine',
        description='Site Engine',
        choices=_my_runtimes, default='php70',
        validators=[
            Required('Please enter an site engine'),
            Length(min=1, max=64)
            ]
    )


