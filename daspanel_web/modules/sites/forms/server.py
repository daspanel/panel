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

_my_server_types = [('caddy', 'Caddy')]

# ============================
# Upload content from remote HTPP url form
# ============================
class ServerCmdForm(FlaskForm):
    """Execute server command
    """
    server_type = SelectField(
        'Target HTTP Server',
        description='Select HTTP server type',
        choices=_my_server_types, default='caddy',
        validators=[
            Required('Please enter an server type'),
            Length(min=1, max=64)
            ]
    )


