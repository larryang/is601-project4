""" fixture to add/delete user """
import pytest
from werkzeug.security import generate_password_hash
from app import db
from app.db.models import User, Transaction

TEST_EMAIL = 'testuser@test.com'
TEST_PASSWORD = 'testtest'
TEST_HASH = generate_password_hash(TEST_PASSWORD)

@pytest.fixture
def test_user(application):
    """ setup database user and delete """

    with application.app_context():
        assert db.session.query(User).count() == 0 # pylint: disable=no-member

        user = User(TEST_EMAIL, TEST_HASH)
        db.session.add(user) # pylint: disable=no-member
        db.session.commit() # pylint: disable=no-member

        yield user

        # delete user and verify
        db.session.delete(user) # pylint: disable=no-member
        assert db.session.query(User).count() == 0 # pylint: disable=no-member
        assert db.session.query(Transaction).count() == 0 # pylint: disable=no-member
