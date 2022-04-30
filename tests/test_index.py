""" test for index page """
# pylint: disable=redefined-outer-name
import datetime
import re
from os import getenv
import pytest

@pytest.fixture()
def resp(client):
    """ get home/index page """
    return client.get("/")


def test_context_variables_environment(resp):
    """This test checks if the environment is printed"""
    env = getenv('FLASK_ENV', None)
    test_string = f"Environment: {env}"
    content = bytes(test_string, 'utf-8')
    assert resp.status_code == 200
    assert content in resp.data


def test_context_variables_year(resp):
    """This tests checks if the copyright and current year are printed"""
    now = datetime.datetime.now()
    year = now.date().strftime("%Y")
    test_string = f"Copyright: {year}"
    content = bytes(test_string, 'utf-8')
    assert resp.status_code == 200
    assert content in resp.data


def test_navbar(resp):
    """ tests navbar """
    data = resp.data

    def match_nav(text):
        """ use regular expression to verify navbar link """
        regex = f"<a class=\\\"nav-item nav-link.*\\n\\s*href=\\\"{text}" # pylint: disable=line-too-long
        my_regex = re.compile(regex)
        return my_regex.search(data.decode('utf-8'))

    assert resp.status_code == 200
    assert match_nav("/")
    assert match_nav("/about")
    assert match_nav("/login")
    assert match_nav("/register")

    # because regular expressions are tricky, make sure it can fail
    assert not match_nav("/foobar")
