""" logging configuration """
import logging
from logging.config import dictConfig
import os
import json
import flask
from flask import current_app
import app
from app import config

log_conf = flask.Blueprint('log_conf', __name__)


def add_path_to_logfile(logdir, logging_config):
    """ add logging path to logging filename """
    # TODO refactor to use template JSON, probably jinja2
    handlers = logging_config['handlers']
    for handler_key in handlers:
        handler = handlers[handler_key]
        if 'filename' in handler:
            log_filename = os.path.join(logdir, handler['filename'])
            logging_config['handlers'][handler_key]['filename'] = log_filename


@log_conf.before_app_first_request
def setup_logs():
    """ before app startup logging config """

    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, 'logging_config.json')
    with open(filepath, encoding="utf-8") as file:
        logging_config = json.load(file)

    logdir = current_app.config['LOG_DIR']
    add_path_to_logfile(logdir, logging_config)

    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)

    # configure logger with JSON file
    logging.config.dictConfig(logging_config)

    # log to logfile misc_debug.log
    log = logging.getLogger("misc_debug")
    log.debug("Configured logging for ENV=%s", current_app.config["ENV"])
