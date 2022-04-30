"""A simple flask web app"""
import os
import flask
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5 # pylint: disable=no-name-in-module
from flask_cors import CORS
import flask_login
from flask_wtf.csrf import CSRFProtect
from app.auth import auth
from app.cli import create_database
from app.db import database, db
from app.db.models import User
from app.simple_pages import simple_pages
from app.util.logger_config import log_conf
from app.util.context_processor import utility_context_processor

login_manager = flask_login.LoginManager()


def page_not_found(e):
    """ handle 404 """
    # pylint: disable=invalid-name
    # TODO log e when logging implemented
    return render_template("404.html"), 404


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    #----------------------------------------
    # basic config
    #
    if  os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")

    app.context_processor(utility_context_processor)
    app.register_blueprint(log_conf)

    #----------------------------------------
    # web stuff
    #
    bootstrap = Bootstrap5(app) # pylint: disable=unused-variable

    # setup database
    app.register_blueprint(database)
    db.init_app(app)

    # login/security
    # https://flask-login.readthedocs.io/en/latest/  <-login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Needed for CSRF protection of form submissions and WTF Forms
    # https://wtforms.readthedocs.io/en/3.0.x/
    csrf = CSRFProtect(app)
    api_v1_cors_config = {
        "methods": ["OPTIONS", "GET", "POST"],
    }
    CORS(app, resources={"/api/*": api_v1_cors_config})

    # load routes/webpages
    app.register_error_handler(404, page_not_found)
    app.register_blueprint(simple_pages)
    app.register_blueprint(auth)

    #----------------------------------------
    # add command function to cli commands
    #
    app.cli.add_command(create_database)

    return app


@login_manager.user_loader
def user_loader(user_id):
    """  callback function """
    # https://flask-login.readthedocs.io/en/latest/#how-it-works

    try:
        return User.query.get(int(user_id))
    except: # pylint: disable=bare-except
        return None
