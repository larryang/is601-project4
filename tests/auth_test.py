"""This test authorization pages"""
from tests.user_fixture import test_user, TEST_EMAIL, TEST_PASSWORD, add_transaction # pylint: disable=unused-import


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
    assert test_user.is_authenticated()


def test_dashboard(application, test_user, add_transaction):
    """ test access to dashboard when logged in """
    # pylint: disable=redefined-outer-name,unused-argument

    with application.test_client(user=test_user) as client:
        resp = client.get('/dashboard')

    # check if successful at getting /dashboard
    assert resp.status_code == 200
    assert b'<h2>Dashboard</h2>' in resp.data
    assert b'<p>Welcome: testuser@test.com</p>' in resp.data

    # check balance
    assert b'<p>Account Balance: 85.00 </p>' in resp.data

    # verify table
    assert b'<th scope="col">Amount</th>' in resp.data
    assert b'<th scope="col">User Id</th>' in resp.data
    assert b'<th scope="col">Transaction Type</th>' in resp.data


def test_logout(client, test_user):
    """ GET to login """
    # pylint: disable=unused-argument,redefined-outer-name

    resp = client.get('/logout')

    # if login, redirect to index
    assert resp.status_code == 302
    assert b'<h1>Redirecting...</h1>' in resp.data
    assert test_user.is_authenticated() is False
