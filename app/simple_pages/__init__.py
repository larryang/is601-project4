""" Render Simple Pages"""
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app.auth.forms import login_form

simple_pages = Blueprint('simple_pages', __name__, template_folder='templates')

@simple_pages.route('/')
def index():
    """ root index.html """
    try:
        return render_template('index.j2.html', form=login_form())
    except TemplateNotFound:
        abort(404)


@simple_pages.route('/about')
def about():
    """ about.html """
    try:
        return render_template('about.j2.html')
    except TemplateNotFound:
        abort(404)
