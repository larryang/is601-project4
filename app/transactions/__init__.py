""" transactions module """
from csv import DictReader
import logging
import os
from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from jinja2 import TemplateNotFound
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

@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():
    """ use form to upload song list CSV """
    log = logging.getLogger("upload_transactions")
    form = CsvUpload()

    try:
        return render_template('upload_transactions.j2.html', form=form)
    except TemplateNotFound:
        abort(404)
