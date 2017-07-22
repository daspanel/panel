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
                                StopValidation, Length, Regexp)

from daspanel_web.lib.wtform_helpers import NoPreValidationSelectField

#from wtforms.widgets import PasswordInput, CheckboxInput
#from daspanel_web.lib.util import verify_password_hash

#_my_types = [
#    ('generic', 'Generic site'), 
#    ('grav', 'Grav'), 
#    ('wordpress', 'Wordpress'),
#    ('cakephp2x', 'CakePHP 2.X'),
#    ('nextcloud12x', 'Nextcloud 12.X')
#]
#_my_runtimes = [
#    ('php71', 'PHP 7.1'), 
#    ('php70', 'PHP 7.0'), 
#    ('php56', 'PHP 5.6'),
#    ('static', 'Static')
#]
_my_confirmation = [('no', 'NO'), ('yes', 'YES')]

# ============================
# Confirmation form
# ============================
class DeleteSiteForm(FlaskForm):
    """Confirm operation form
    """
    confirm = SelectField(
        'You really want to delete this site ?',
        description='You really want to delete this site ?',
        choices=_my_confirmation, default='no',
        validators=[
            Required('Please confirm site delete'),
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
class NewSiteForm(FlaskForm):
    """Create site form
    """
    sitedescription = TextField(
        'Description',
        description='Site Description',
        validators=[
            Required('Please enter an site description'),
            Length(min=1, max=255)
            ])
    sitetype = NoPreValidationSelectField(
        'Type',
        description='Site Type',
        choices=[],
        validators=[
            Required('Please enter an site type'),
            Length(min=1, max=64)
            ]
    )
    runtime = NoPreValidationSelectField(
        'Engine',
        description='Site Engine',
        choices=[],
        validators=[
            Required('Please enter an site engine'),
            Length(min=1, max=64)
            ]
    )

    #def validate_sitetype(form, field):
    #    """Check if site type is valid
    #    """
    #    if field.data not in ['grav']:
    #        raise ValidationError('grav is the only allowed site type')


class EditSiteForm(FlaskForm):
    """Create site form
    """
    sitedescription = TextField(
        'Description',
        description='Site Description',
        validators=[
            Required('Please enter an site description'),
            Length(min=1, max=255)
            ]
    )
    urlprefix = TextField(
        'Url Prefix',
        description='Url prefix',
        validators=[
            Required('Please enter an url prefix description'),
            Length(min=1, max=255),
            Regexp('^[a-zA-Z0-9_-]+$', 
                message='Invalid prefix. Only letters and numbers allowed')
            ]
    )



