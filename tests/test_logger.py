""" test logger configuration """
import os
import json
import app.config
from app.util.logger_config import add_path_to_logfile

LOGDIR = app.config.Config.LOG_DIR

def test_add_path_to_logfile():
    """ test function to add path to logger filename """
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(path, '../app/util/logger_config/logging_config.json')
    with open(filepath, encoding="utf-8") as file:
        logging_config = json.load(file)

    # add logging path to logging filename
    add_path_to_logfile(LOGDIR, logging_config)

    flask_log = os.path.join(LOGDIR, 'flask.log')
    assert logging_config['handlers']['file.handler']['filename'] == flask_log


def test_logfile_exists():
    """ check if logfiles exist """

    def verify_logfile(filename):
        """ helper function """
        filepath = os.path.join(LOGDIR, filename)
        return os.path.isfile(filepath)

    assert verify_logfile('flask.log')
    assert verify_logfile('misc_debug.log')
    assert verify_logfile('request.log')
    assert verify_logfile('sqlalchemy.log')
    assert verify_logfile('upload_transactions.log')
    assert verify_logfile('werkzeug.log')


def test_misc_debug_log():
    """" check if capturing start up message """
    filepath = os.path.join(LOGDIR, 'misc_debug.log')

    with open(filepath, encoding="utf-8") as file:
        assert '[DEBUG] misc_debug: [testing] Configured logging' in file.read()
