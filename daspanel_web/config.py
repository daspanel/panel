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
from devourer import GenericAPI, APIMethod, APIError

class ConfigApi(GenericAPI):
    get_config   = APIMethod('get', '/{id}')

    def __init__(self, server='http://daspanel-api:8080/1.0', auth=None):
        _headers = {
            'pragma': 'no-cache',
            'Connection': 'close',
            'Accept': 'application/json',
            'Authorization': auth,
        }

        super(ConfigApi, self).__init__(
            url = '{}/tenants'.format(server),
            auth = None,
            headers = _headers,
            load_json = True,
            throw_on_error = True
        )
        
    def finalize(self, name, result, *args, **kwargs):
        if self.throw_on_error and result.status_code >= 400:
            raise APIError(json.loads(result.content)['detail'], response=result.__dict__)
        if self.load_json:
            return json.loads(result.content)
        return result.content

# Daspanel
DASPANEL_SYS_UUID = os.environ.get('DASPANEL_SYS_UUID')
DASPANEL_SYS_APISERVER = os.getenv('DASPANEL_SYS_APISERVER', 'http://daspanel-api:8080/1.0')
DASPANEL_DATADIR = os.path.join('/opt/daspanel/data', DASPANEL_SYS_UUID)

api = ConfigApi(server=DASPANEL_SYS_APISERVER, auth=DASPANEL_SYS_UUID)
try:
    DASPANEL = api.get_config(id=DASPANEL_SYS_UUID)
except APIError as err:
    #print('[DASPANEL-PANEL] Error getting system configuration: {0}'.format(str(err)), file=sys.stderr)
    raise Exception('[DASPANEL-PANEL] Error getting system configuration: {0}'.format(str(err)))

if DASPANEL["sys"]["debug"] == 'True':
    DASPANEL_DEBUG = True
else:
    DASPANEL_DEBUG = False

# Global
DEBUG = DASPANEL_DEBUG
SECRET_KEY = DASPANEL_SYS_UUID
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# Flask toolbar debug
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = True

# SQLAlchemy
APP_DATABASE = 'daspanel-web.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DASPANEL_DATADIR, 'db', APP_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Will be false in Flask-SQLA v3

# Flask-Mail
smtp_server = DASPANEL["smtp"]["server"].split(':')
MAIL_USE_TLS = False
MAIL_DEFAULT_SENDER = 'Flaskapp <' + DASPANEL["smtp"]["user"] + '>'

if len(smtp_server) > 1:
    MAIL_PORT = int(smtp_server[1])
else:
    MAIL_PORT = 587

MAIL_SERVER = smtp_server[0]
MAIL_USERNAME = DASPANEL["smtp"]["user"]
MAIL_PASSWORD = DASPANEL["smtp"]["password"]
MAIL_DEBUG = False


