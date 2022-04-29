""" Test application configuration """
# project/tests/test_config.py


def test_development_config(application):
    """ config for Development Server deploy """
    application.config.from_object('app.config.DevelopmentConfig')
    assert application.config['DEBUG']
    assert not application.config['TESTING']


def test_testing_config(application):
    """ config for local testing """
    application.config.from_object('app.config.TestingConfig')
    assert application.config['DEBUG']
    assert application.config['TESTING']
    assert not application.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert application.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'


def test_production_config(application):
    """ config for Production Server deploy """
    application.config.from_object('app.config.ProductionConfig')
    assert not application.config['DEBUG']
    assert not application.config['TESTING']
