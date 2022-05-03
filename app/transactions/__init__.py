""" transactions module """
from csv import DictReader
import logging
import os
from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from jinja2 import TemplateNotFound
import werkzeug
import wtforms
from app import db
from app.db.models import Transaction, TransactionTypeEnum

def open_and_parse_csv(filepath):
    """ utility function to open and parse a CSV """
    transaction_list = []
    log = logging.getLogger("upload_transactions")

    with open(filepath, encoding="utf-8-sig" ) as file:
        csv_table = DictReader(file, dialect='excel')
        log.info("[%s] opened and parsing filepath:[%s]",
            current_user, filepath)

        log.info("CSV: %s, Fieldnames: %s", filepath, csv_table.fieldnames)

        # TODO check CSV for proper headers
        csv_header = Transaction.csv_headers()
        for row in csv_table:
            amount = row[csv_header[0]]
            transaction_type = TransactionTypeEnum[row[csv_header[1]]]

            transaction_list.append(Transaction(amount, transaction_type))

    return transaction_list


class CsvUpload(FlaskForm):
    """ form for uploading CSV"""
    file = wtforms.FileField()
    submit = wtforms.SubmitField()


transactions = Blueprint('transactions', __name__,
                        template_folder='templates')


@transactions.before_app_first_request
def setup_upload():
    """ create upload directory """
    logdir = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(logdir):
        os.mkdir(logdir)

@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():
    """ use form to upload song list CSV """
    log = logging.getLogger("upload_transactions")
    form = CsvUpload()

    if request.method == 'POST':
        if form.validate_on_submit():
            filename = werkzeug.utils.secure_filename(form.file.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.file.data.save(filepath)
            transactions_list = open_and_parse_csv(filepath)

            current_user.transactions += transactions_list # pylint: disable=assigning-non-slot
            db.session.commit() # pylint: disable=no-member

            return redirect(url_for('auth.dashboard'))
        else:
            log.info("form failed validation")

    try:
        return render_template('upload_transactions.j2.html', form=form)
    except TemplateNotFound:
        abort(404)
