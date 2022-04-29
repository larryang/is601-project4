"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import os
import pytest
from flask import Flask
from flask_login import FlaskLoginClient
from app import create_app
from app.db import db



@pytest.fixture()
def application():
    """This makes the app"""
    #you need to run it in testing to pass on github
    os.environ['FLASK_ENV'] = 'testing'

    application = create_app()
    application.test_client_class = FlaskLoginClient
    application.config['WTF_CSRF_ENABLED'] = False

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()


def test_application_instance(application):
    """ Test application is an instance """
    assert isinstance(application, Flask)
