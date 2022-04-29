"""A simple flask web app"""
import os
import flask
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5 # pylint: disable=no-name-in-module
from app.cli import create_database
from app.db import database, db
from app.db.models import User
from app.simple_pages import simple_pages
from app.util.logger_config import log_conf
from app.util.context_processor import utility_context_processor


def page_not_found(e):
    """ handle 404 """
    # pylint: disable=invalid-name
    # TODO log e when logging implemented
    return render_template("404.html"), 404


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if  os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")

    app.register_error_handler(404, page_not_found)
    app.context_processor(utility_context_processor)
    app.register_blueprint(log_conf)


    #----------------------------------------
    # web stuff
    bootstrap = Bootstrap5(app) # pylint: disable=unused-variable

    # load routes/webpages
    app.register_blueprint(simple_pages)

    # setup database
    app.register_blueprint(database)
    db.init_app(app)

    # login/security


    #----------------------------------------
    # add command function to cli commands
    app.cli.add_command(create_database)
    
    return app
