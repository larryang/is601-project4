""" application context processor """
from os import getenv
from datetime import datetime

def utility_context_processor():
    """ misc utilities for flask app context """

    def deployment_environment():
        """ implement deployment_environment """
        return getenv('FLASK_ENV', None)

    def current_year():
        now = datetime.now()
        date = now.date()
        year = date.strftime("%Y")
        return year

    return dict(
        deployment_environment = deployment_environment(),
        year = current_year()
    )
