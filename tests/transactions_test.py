""" test transactions model """
import os
from flask import current_app
from app import config, db
from app.db.models import Transaction, TransactionTypeEnum
from app.transactions import open_and_parse_csv
from tests.user_fixture import test_user, TEST_EMAIL, add_transaction # pylint: disable=unused-import

def test_modify_transactions(application, test_user, add_transaction):
    """ test basic db stuff """
    # pylint: disable = redefined-outer-name, unused-argument
    assert db.session.query(Transaction).count() == 2 # pylint: disable=no-member

    # read
    trans1 = Transaction.query.filter_by(
        transaction_type = TransactionTypeEnum.CREDIT
        ).first()
    assert trans1.amount == 100

    # write
    trans1.amount = 200
    db.session.commit() # pylint: disable=no-member
    trans2 = Transaction.query.filter_by(amount=200).first()
    assert trans2.transaction_type == TransactionTypeEnum.CREDIT

    # delete
    db.session.delete(trans2) # pylint: disable=no-member
    db.session.commit() # pylint: disable=no-member
    assert db.session.query(Transaction).count() == 1 # pylint: disable=no-member


def test_load_transactions_csv(test_user):
    """ open csv file and load into database """
    # pylint: disable = redefined-outer-name
    assert db.session.query(Transaction).count() == 0 # pylint: disable=no-member

    base_dir = current_app.config["BASE_DIR"]
    filename = 'transactions.csv'
    filepath = base_dir + '/../tests/' + filename

    transaction_list = open_and_parse_csv(filepath)
    test_user.transactions += transaction_list

    assert db.session.query(Transaction).count() == 28 # pylint: disable=no-member

    item = Transaction.query.filter_by(amount=-2324).first() # pylint: disable=no-member
    assert item.transaction_type == TransactionTypeEnum.DEBIT


def test_get_transactions_upload_auth(application, test_user):
    """ access page while auth"""
    # pylint: disable=unused-argument,redefined-outer-name

    root = config.Config.BASE_DIR
    filename = 'transactions.csv'
    filepath = os.path.join(root, '../tests/', filename)

    # cleanup upload
    upload_folder = config.Config.UPLOAD_FOLDER
    upload_file = os.path.join(upload_folder, filename)
    if os.path.exists(upload_file):
        os.remove(upload_file)

    with application.test_client(user=test_user) as client:
        resp = client.get("/transactions/upload")
        assert resp.status_code == 200
        assert b'<h2>Upload Transactions</h2>' in resp.data

        with open(filepath, 'rb') as file:
            data = {
                'file': (file, filename),
                #'csrf_token': current_
            }
            resp = client.post('/transactions/upload', data=data)

    assert db.session.query(Transaction).count() == 28 # pylint: disable=no-member

    item = Transaction.query.filter_by(amount=-2324).first() # pylint: disable=no-member
    assert item.transaction_type == TransactionTypeEnum.DEBIT

    # check to capture logging of CSV parsing
    logdir = current_app.config['LOG_DIR']
    filepath = os.path.join(logdir, 'upload_transactions.log')
    with open(filepath, encoding="utf-8") as file:
        assert '[<User testuser@test.com>] opened and parsing filepath:[' in file.read()
