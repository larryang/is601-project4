""" decorator to enforce admin privilege"""
from functools import wraps
from flask_login import current_user
from flask import render_template

def admin_required(f):
    """ verify if authorized otherwise 403 """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin != 1:
            return render_template('403.j2.html'), 403
        return f(*args, **kwargs)
    return decorated_function
