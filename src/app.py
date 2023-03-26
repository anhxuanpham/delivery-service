# File app.py 
# Created at 24/03/2023
# Author Khanh

"""
   Description:
        -
        -
"""

import sentry_sdk
from pymodm import connect
from sentry_sdk import capture_message
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, request, jsonify
from flask_babel import Babel
from src.api import rest_app
from vibe_library.logger import Logger
from .config import DefaultConfig
from jsonschema import ValidationError

# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = rest_app


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_relative_config=True)
    configure_app(app, config)
    # configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    # configure_template_filters(app)
    # configure_error_handlers(app)
    # configure_logging_level()
    # configure_jobs(app)
    return app


def configure_jobs(app):
    # trigger = AndTrigger([IntervalTrigger(hours=1)])
    # jobs.add_job(
    #     name_job(),
    #     trigger
    # )
    # jobs.start()
    Logger.debug("Init jobs")


def configure_app(app, config=None):
    """Different ways of configurations."""
    app.config.from_object(DefaultConfig)
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)


def configure_extensions(app):
    # flask-sqlalchemy
    # db.init_app(app)
    Logger.debug('Connect with Mysql successfully')

    connect(DefaultConfig.MONGODB_URI, connect=False)
    Logger.error('Connect with MongoDB successfully')
    Logger.error({
        'testing': 1
    })
    # Redis
    # redis_cache.init_app(app)
    Logger.debug('Init Redis cache successfully')
    # Flask Babel
    babel = Babel(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix="{}/{}".format(app.config.get('PREFIX'), blueprint.url_prefix))


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging_level():
    import logging
    logging.getLogger('suds').setLevel(logging.ERROR)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_page(error):
        return jsonify({
            'status': 0,
            'error_code': 'E_FORBIDDEN',
            'msg': 'forbidden',
            'data': {}
        }), 200

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'status': 0,
            'error_code': 'E_NOT_FOUND',
            'msg': 'notfound',
            'data': {}
        }), 200

    @app.errorhandler(500)
    def server_error_page(error):
        return jsonify({
            'status': 0,
            'error_code': 'E_SERVER_ERROR',
            'msg': 'server error',
            'data': {}
        }), 200

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return jsonify({
                'status': 0,
                'error_code': 'E_VALIDATION',
                'msg': original_error.message,
                'data': {}
            }), 200
        return error
