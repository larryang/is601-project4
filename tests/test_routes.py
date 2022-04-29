""" test routes """

def test_request_index(client):
    """This tests the index """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


#when base.html is working properly (current_user is undefined error)
def test_page_not_found(client):
    """This tests getting a 404 for /foobar """
    response = client.get("/foobar]")
    assert response.status_code == 404
    assert b"<h1>404</h1>" in response.data
    assert b"Oops! Looks like the page doesn't exist anymore (or never existed)" in response.data
