""" Database blueprint """
import os
import logging
from flask import Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from app import config

db = SQLAlchemy()

database = Blueprint('database', __name__,)

def create_db_dir():
    """ helper function to check/create db directory """
    log = logging.getLogger("misc_debug")
    root = current_app.config["BASE_DIR"]
    db_dir = os.path.join(root, '..', current_app.config["DB_DIR"])
    if not os.path.exists(db_dir):
        log.debug("[%s] Making database directory %s", current_app.env, db_dir)
        os.mkdir(db_dir)


@database.cli.command('create')
def init_db():
    """ click command to create db """
    create_db_dir()
    db.create_all()


@database.before_app_first_request
def create_db_file_if_does_not_exist():
    """ create db """
    create_db_dir()
    db.create_all()
