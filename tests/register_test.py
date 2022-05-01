"""This test authorization pages"""
from app import db
from app.db.models import User
from tests.user_fixture import test_user  # pylint: disable=unused-import
from tests.user_fixture import TEST_EMAIL, TEST_HASH


def test_add_user(test_user):
    """ test adding a user to database """
    # pylint: disable=redefined-outer-name
    assert db.session.query(User).count() == 1 # pylint: disable=no-member

    user = User.query.filter_by(email=TEST_EMAIL).first()
    assert user.id == 1
    assert user.password == TEST_HASH

    # modify e-mail and make sure same user
    new_email = "newemail@test.com"
    test_user.email = "newemail@test.com"

    new_user = User.query.filter_by(id=1).first()
    assert new_user.email == new_email


def test_register(client):
    """ POST to /register """
    new_email = 'newuser@test.test'
    new_password = 'Test1234!'
    assert not User.query.filter_by(email=new_email).first()

    data = {
        'email' : new_email,
        'password' : new_password,
        'confirm' : new_password
    }
    resp = client.post('/register', data=data)

    assert resp.status_code == 302

    # verify new user is in database
    new_user = User.query.filter_by(email=new_email).first()
    assert new_user.email == new_email

    db.session.delete(new_user) # pylint: disable=no-member
