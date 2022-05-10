""" basic test for routes """
# each page that gets created, add simple GET and make sure it exists
#    additional functionality should be in route specific file
#
#   !!! make sure to add an entry in test_index.py for navbar !!!


import os
from app import config


def test_get_about(client):
    """This tests /about """
    response = client.get("/about")
    assert response.status_code == 200
    assert b"<h1>About</h1>" in response.data


def test_get_dashboard(client):
    """This tests /dashboard """
    # redirect to /login since not authenticated
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data


def test_get_index(client):
    """This tests the index """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Index Page</h1>" in response.data


def test_get_login(client):
    """This tests the login """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data


def test_get_logout(client):
    """This tests the logout """
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data


def test_get_registration(client):
    """ this tests /registration """
    response = client.get("/register")
    assert response.status_code == 200
    assert b"<h2>Register</h2>" in response.data


def test_get_transaction_upload(client):
    """ tests /transactions/upload """
    response = client.get("/transactions/upload")
    # redirect because not authenticated
    assert response.status_code == 302


def test_post_transaction_upload(client):
    """ tests /transactions/upload while unauthorized"""

    root = config.Config.BASE_DIR
    filename = 'transactions.csv'
    filepath = os.path.join(root, '../tests/', filename)

    with open(filepath, 'rb') as file:
        data = {
            'file': (file, filename),
            #'csrf_token': current_
        }
        resp = client.post('/transactions/upload', data=data)

    # redirect because not authenticated
    assert resp.status_code == 302


def test_page_not_found(client):
    """This tests getting a 404 for /foobar """
    response = client.get("/foobar]")
    assert response.status_code == 404
    assert b"<h1>404</h1>" in response.data
    assert b"Oops! Looks like the page doesn't exist anymore (or never existed)" in response.data
