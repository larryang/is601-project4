"""A simple flask web app"""
import os
import flask
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5 # pylint: disable=no-name-in-module
from app.cli import create_database
from app.db import db
from app.db.models import User
from app.simple_pages import simple_pages
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

    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'

    app.register_error_handler(404, page_not_found)
    app.context_processor(utility_context_processor)

    bootstrap = Bootstrap5(app) # pylint: disable=unused-variable

    # load routes/webpages
    app.register_blueprint(simple_pages)

    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # add command function to cli commands
    app.cli.add_command(create_database)

    return app
