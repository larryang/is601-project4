""" implement user authorization/login routes """
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, current_user
from jinja2 import TemplateNotFound
from app.auth.forms import login_form
from app.db import db
from app.db.models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """ login a user (start session) """
    form = login_form()
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome", 'success')
            return redirect(url_for('auth.dashboard'))
    return render_template('login.j2.html', form=form)


@auth.route('/dashboard')
@login_required
def dashboard():
    """ render user's dashboard page """
    try:
        return render_template('dashboard.j2.html')
    except TemplateNotFound:
        abort(404)
