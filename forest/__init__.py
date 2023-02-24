import os
import json
import logging
import logging.config

from flask import Flask

from . import auth_bp
from . import home_bp
from . import forest_bp
from . import db
from . import guard
from . import lumber

logger = logging.getLogger(__name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='c8a2d2ebfd7a97fedf84756e69347af354c8b2bcacb1a2bc8277c59688879c03',
        DATABASE=os.path.join(app.instance_path, 'forest.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # create the log directory
    log_path = os.path.join(app.instance_path, 'logs')
    try:
        os.makedirs(log_path)
    except OSError:
        pass

    # read logging configuration
    log_config_file = os.path.join(app.instance_path, 'logging.json')
    with open(log_config_file) as f:
        log_config = json.load(f)

    # set the logging file name
    log_config['handlers']['file']['filename'] = os.path.join(log_path, 'forest.log')
    logging.config.dictConfig(log_config)

    db.register(app)

    lumber.register(app)

    app.before_request(guard.load_person)

    app.register_blueprint(forest_bp.bp)
    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(home_bp.bp)

    return app
