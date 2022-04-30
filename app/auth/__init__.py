""" implement user authorization/login routes """
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, current_user
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash

from app.auth import forms
from app.db import db
from app.db.models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """ login a user (start session) """
    form = forms.login_form()
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


@auth.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """ render user's dashboard page """
    try:
        return render_template('dashboard.j2.html')
    except TemplateNotFound:
        abort(404)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    """ register route """

    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))

    form = forms.register_form()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            user = User(email=form.email.data, password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()

            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()

            flash('Congratulations, you are now a registered user!', "success")
            return redirect(url_for('auth.login'), 302)
        else:
            flash('Already Registered')
            return redirect(url_for('auth.login'), 302)

    return render_template('register.j2.html', form=form)
