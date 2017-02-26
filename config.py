import os
import ast
import datetime

#basedir = os.path.abspath(os.path.dirname(__file__))
#basedir = os.path.join('/opt/daspanel/data', os.environ.get('DASPANEL_GUUID'))

# Daspanel
DASPANEL_DATADIR = os.path.join('/opt/daspanel/data', os.environ.get('DASPANEL_GUUID'))
DASPANEL_UUID = os.environ.get('DASPANEL_GUUID')
DASPANEL_HOST = os.environ.get('DASPANEL_HOST', 'daspanel.site')
if os.environ.get('DASPANEL_DEBUG', 'False') == 'True':
    DASPANEL_DEBUG = True
else:
    DASPANEL_DEBUG = False

# Global
DEBUG = DASPANEL_DEBUG
SECRET_KEY = os.environ.get('DASPANEL_GUUID', os.urandom(25).encode('hex'))
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# Flask toolbar debug
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = True

# SQLAlchemy
APP_DATABASE = 'daspanel-web.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DASPANEL_DATADIR, 'db', APP_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Will be false in Flask-SQLA v3

# Flask-Mail
smtp_server = os.environ.get('DASPANEL_MAIL_SERVER', 'smtp.gmail.com:587').split(':')
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = 'Flaskapp <' + os.environ.get('DASPANEL_MAIL_USER') + '>'

if len(smtp_server) > 1:
    MAIL_PORT = smtp_server[1]
else:
    MAIL_PORT = 587

MAIL_SERVER = smtp_server[0]
MAIL_USERNAME = os.environ.get('DASPANEL_MAIL_USER')
MAIL_PASSWORD = os.environ.get('DASPANEL_MAIL_PWD')
MAIL_DEBUG = False



