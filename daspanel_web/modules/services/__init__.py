#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Daspanel CP services module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sservices module for Daspanel web control panel.

:copyright: (c) 2017 by Abner G Jacobsen
:licence: GNU General Public License v3, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function
import logging

__title__ = 'Daspanel services module'
__summary__ = 'Sites module for Daspanel web control panel.'
__uri__ = 'https://github.com/daspanel/cpweb'

__version__ = '0.0.1'

__author__ = 'Abner G Jacobsen'
__email__ = 'abner@apoana.com.br'

__license__ = 'GNU General Public License v3'
__copyright__ = 'Copyright 2017 Abner G Jacobsen'

# the user should dictate what happens when a logging event occurs
#logging.getLogger(__name__).addHandler(logging.NullHandler())

"""The content module."""
__all__ = ["views"]
from .views import *  # noqa


