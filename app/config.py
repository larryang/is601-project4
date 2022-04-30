""" Configure environmental variables """
# pylint: disable=too-few-public-methods
import os


class Config(object):
    """ base configuration """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    SESSION_COOKIE_SECURE = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'Simplex'
    DB_DIR = os.getenv('DB_DIR','database')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR,'..', DB_DIR, "db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER =  os.getenv('UPLOAD_FOLDER', BASE_DIR + '/uploads')
    LOG_DIR =  os.path.join(BASE_DIR, '../logs')


class ProductionConfig(Config):
    """" subclass for production server """


class DevelopmentConfig(Config):
    """ configuration for development server """
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """ configuration to use for local testing """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SESSION_COOKIE_SECURE = False
    DEBUG = True
