""" Database blueprint """
import os
import logging
from flask import Blueprint, cli
from flask_sqlalchemy import SQLAlchemy
from app import config

db = SQLAlchemy()

database = Blueprint('database', __name__,)


@database.cli.command('create')
def init_db():
    """ click command to create db """
    db.create_all()


@database.before_app_first_request
def create_db_file_if_does_not_exist():
    """ create db """
    log = logging.getLogger("misc_debug")

    root = config.Config.BASE_DIR
    # set the name of the apps log folder to logs
    db_dir = os.path.join(root, '..', config.Config.DB_DIR)
    # make a directory if it doesn't exist
    if not os.path.exists(db_dir):
        log.debug("Making database directory %s", db_dir)
        os.mkdir(db_dir)
    db.create_all()
