#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Daspanel CP Web

Daspanel control panel for web

 :copyright: (c) 2017, Abner G Jacobsen.
             All rights reserved.
 :license:   GNU General Public License v3, see LICENSE for more details.
"""
from __future__ import absolute_import, division, print_function
import os
import ast
import datetime
import json

#basedir = os.path.abspath(os.path.dirname(__file__))
#basedir = os.path.join('/opt/daspanel/data', os.environ.get('DASPANEL_SYS_UUID'))


# Daspanel
DASPANEL_UUID = os.environ.get('DASPANEL_SYS_UUID')
DASPANEL_DATADIR = os.path.join('/opt/daspanel/data', DASPANEL_UUID)
conf_file = os.path.join(DASPANEL_DATADIR, 'db', 'sysconfig.json')
sys_config = json.loads(open(conf_file).read())

DASPANEL_HOST = sys_config["sys"]["hostname"]

if sys_config["sys"]["debug"] == 'True':
    DASPANEL_DEBUG = True
else:
    DASPANEL_DEBUG = False

# Global
DEBUG = DASPANEL_DEBUG
SECRET_KEY = DASPANEL_UUID
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# Flask toolbar debug
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = True

# SQLAlchemy
APP_DATABASE = 'daspanel-web.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DASPANEL_DATADIR, 'db', APP_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Will be false in Flask-SQLA v3

# Flask-Mail
smtp_server = sys_config["smtp"]["server"].split(':')
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'Flaskapp <' + sys_config["smtp"]["user"] + '>'

if len(smtp_server) > 1:
    MAIL_PORT = smtp_server[1]
else:
    MAIL_PORT = 587

MAIL_SERVER = smtp_server[0]
MAIL_USERNAME = sys_config["smtp"]["user"]
MAIL_PASSWORD = sys_config["smtp"]["password"]
MAIL_DEBUG = False



