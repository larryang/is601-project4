import click
from flask.cli import with_appcontext
from app.db import db, create_db_dir


@click.command(name='create-db')
@with_appcontext
def create_database():
    """ create database """
    create_db_dir()
    db.create_all()
    