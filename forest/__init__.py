import json
import logging
import logging.config
import os

from flask import Flask, flash, redirect, url_for

from . import dart, db, lumber, guard
from . import forest_bp, auth_bp, home_bp

logger = logging.getLogger(__name__)


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'forest.sqlite'),
    )

    if test_config is None:
        # Load the regular config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if present
        app.config.from_mapping(test_config)

    # Create the instance and log folders
    log_folder = os.path.join(app.instance_path, 'logs')
    try:
        os.makedirs(log_folder)
    except OSError:
        pass

    # Read the logging configuration
    log_config_file = os.path.join(__name__, 'logging.json')
    with open(log_config_file) as f:
        log_config = json.load(f)

    # Define the log file name and set the logging configuration
    log_config['handlers']['file']['filename'] = os.path.join(log_folder, 'forest.log')
    logging.config.dictConfig(log_config)

    # Register the database
    db.register(app)

    # Enable the command line tools
    lumber.register(app)

    # Put the authenticated user, if present, into every request
    app.before_request(guard.load_person)

    # Register our custom template functions
    app.jinja_env.globals['csrf_token'] = guard.csrf_token
    app.jinja_env.globals['has_role'] = guard.has_role
    app.jinja_env.globals['dart_has'] = dart.dart_has
    app.jinja_env.globals['dart_first'] = dart.dart_first

    # Define all the routes
    app.register_blueprint(forest_bp.bp)
    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(home_bp.bp)

    # Error handlers
    @app.errorhandler(401)
    def handle_401(e):
        return redirect(url_for('auth.login'))

    @app.errorhandler(403)
    def handle_403(e):

        if e.description == 'invalid_token':
            endpoint = 'auth.login'
            flash('Please login again to refresh your session', 'invalid_token')
        else:
            endpoint = 'home.index'
            flash('Your account is not authorized to perform that action', 'not_authorized')

        return redirect(url_for(endpoint))

    return app
