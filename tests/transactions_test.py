""" test transactions model """
from app import db
from app.db.models import Transaction
from tests.user_fixture import test_user, TEST_EMAIL # pylint: disable=unused-import

def test_modify_transactions(application, test_user):
    """ test basic db stuff """
    user = test_user
    assert db.session.query(Transaction).count() == 0 # pylint: disable=no-member

    # write
    transactions = []
    transactions.append( Transaction(100, 'Deposit') )
    transactions.append( Transaction(20, 'Withdrawl') )

    user.transactions += transactions
    db.session.commit() # pylint: disable=no-member
    assert db.session.query(Transaction).count() == 2 # pylint: disable=no-member

    # read
    trans1 = Transaction.query.filter_by(transaction_type='Deposit').first()
    assert trans1.amount == 100

    # write
    trans1.amount = 200
    db.session.commit() # pylint: disable=no-member
    trans2 = Transaction.query.filter_by(amount=200).first()
    assert trans2.transaction_type == 'Deposit'

    # delete
    db.session.delete(trans2) # pylint: disable=no-member
    db.session.commit() # pylint: disable=no-member
    assert db.session.query(Transaction).count() == 1 # pylint: disable=no-member
