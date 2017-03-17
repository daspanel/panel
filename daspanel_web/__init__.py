import os
import json
import logging
import pkg_resources

import cssutils
from flask import Flask, g
from flask_wtf import CSRFProtect
from flask_login import current_user
from flask_principal import Principal, UserNeed, identity_loaded
from flask_debugtoolbar import DebugToolbarExtension

from daspanel_web.lib import template_helpers
from daspanel_web.lib.util import generate_password_hash
from daspanel_web.meta import mail, db, lm
from daspanel_web.modules.auth.models import User
from daspanel_web.modules import content, auth, sites, module1

# suppress cssutils warning messages
cssutils.log.setLevel(logging.CRITICAL)


# ================================
# App creator method
# ================================
def create_app(extra_config=None):
    """Create Flask app for Flaskapp
    """
    app = Flask('daspanel_web',
                template_folder='templates/default',
                static_folder='templates/default/static')

    app.config.from_object('config')
    app.config.update(**(extra_config or {}))
    app.before_request(before_request)

    # the toolbar is only enabled in debug mode:
    #app.debug = True
    #app.config['SECRET_KEY'] = os.environ.get('DASPANEL_SYS_UUID', os.urandom(25).encode('hex'))
    #app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    #app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    if app.config['DEBUG'] == True:
        print("debug enabled")
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)
    else:
        print("debug disabled")

    # import static file manifest
    js = pkg_resources.resource_string('daspanel_web', '/templates/default/static/rev-manifest.json')
    app.config['static_manifest'] = json.loads(js)

    # configure jinja2
    app.jinja_env.globals.update({'h': template_helpers})

    # add Flask-WTForms CSRF Protection
    CSRFProtect(app)

    # init Flask-SQLAlchemy
    db.init_app(app)
    if not os.path.exists(os.path.join(app.config['DASPANEL_DATADIR'], 'db', app.config['APP_DATABASE'])):
        print("Creating database file: " + os.path.join(app.config['DASPANEL_DATADIR'], 'db', app.config['APP_DATABASE']))
        with app.app_context():
            db.create_all()

    conf_file = os.path.join(app.config['DASPANEL_DATADIR'], 'db', 'sysconfig.json')
    sys_config = json.loads(open(conf_file).read())

    with app.app_context():
        update_or_create_admin(
            sys_config["sys"]["admin"], 
            sys_config["sys"]["password"]
        )

    # init Flask-Principal
    Principal(app)
    identity_loaded.connect(on_identity_loaded, app)

    # init Flask-Login
    lm.init_app(app)
    lm.login_view = 'auth.login'
    lm.user_loader(load_user)

    # init Flask-Mail
    mail.init_app(app)

    # register blueprints
    app.register_blueprint(content.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(sites.bp, url_prefix='/sites')
    app.register_blueprint(module1.bp, url_prefix='/module1')

    return app


# ===============================
# Helper methods
# ===============================
def update_or_create_admin(email, password):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        print("Creating admin user: " + email)
        user = User(email=email,
                    password=generate_password_hash(password),
                    is_verified=True)
        db.session.add(user)
        db.session.flush()
    else:
        print("Reseting admin user password: " + email)
        user.password = generate_password_hash(password)
        db.session.add(user)
        db.session.flush()

    return user

def before_request():
    """Add current user to g object
    """
    g.user = current_user


def load_user(id):
    """Method for LoginManager user_loader method
    """
    return User.query.get(int(id))


def on_identity_loaded(sender, identity):
    """Method for Flask Principal identity load listener
    """
    # set the identity user object
    identity.user = current_user

    if current_user.is_authenticated:
        # add UserNeed to identity
        identity.provides.add(UserNeed(current_user.id))
