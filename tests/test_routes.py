""" basic test for routes """
# each page that gets created, add simple GET and make sure it exists
#    additional functionality should be in route specific file


def test_get_index(client):
    """This tests the index """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Index Page</h1>" in response.data


def test_get_login(client):
    """This tests the index """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<h2>Login</h2>" in response.data


def test_get_about(client):
    """This tests /about """
    response = client.get("/about")
    assert response.status_code == 200
    assert b"<h1>About</h1>" in response.data



def test_page_not_found(client):
    """This tests getting a 404 for /foobar """
    response = client.get("/foobar]")
    assert response.status_code == 404
    assert b"<h1>404</h1>" in response.data
    assert b"Oops! Looks like the page doesn't exist anymore (or never existed)" in response.data
