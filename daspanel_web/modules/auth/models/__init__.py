#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
flaskapp auth module
~~~~~~~~~~~~~~~~~~~~

Contains all the code you need for an Flaskapp auth module models.

:copyright: (c) 2016 by Abner G Jacobsen
:licence: The MIT License (MIT), see LICENCE for more details
"""
from __future__ import absolute_import, division, print_function
import logging

__title__ = 'flaskapp auth module'
__summary__ = 'Contains all the code you need for an Flaskapp auth module models.'
__uri__ = 'https://github.com/daspanel/flaskapp-cookiecutter'

__version__ = '0.0.1'

__author__ = 'Abner G Jacobsen'
__email__ = 'abner@apoana.com.br'

__license__ = 'The MIT License (MIT)'
__copyright__ = 'Copyright 2016 Abner G Jacobsen'

# the user should dictate what happens when a logging event occurs
#logging.getLogger(__name__).addHandler(logging.NullHandler())

"""The content module."""
__all__ = [
    "sqla"
]
from .sqla import *  # noqa

