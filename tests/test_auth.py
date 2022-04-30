"""This test authorization pages"""
from tests.user_fixture import test_user, TEST_EMAIL, TEST_PASSWORD # pylint: disable=unused-import


def test_login(client, test_user):
    """ POST to login """
    # pylint: disable=unused-argument,redefined-outer-name

    data = {
        'email' : TEST_EMAIL,
        'password' : TEST_PASSWORD
    }
    resp = client.post('/login',
            data=data)

    # if login, redirect to /dashboard
    assert resp.status_code == 302
    assert b'<h1>Redirecting...</h1>' in resp.data
