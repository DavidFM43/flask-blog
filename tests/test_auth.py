import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    # test template rendered successfully
    assert client.get('/auth/register').status_code == 200
    # TODO: Play with the Response object a little bit
    response = client.post('/auth/register',
                           data={'username': 'a', 'password': 'a'})
    # test redirection to login page
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        # test user has been saved on db
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'"
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'),(
                         ('', '', b'Username is required.'),
                         ('a', '', b'Password is required.'),
                         ('test', 'test', b'User test is already taken.'),
))
def test_register_validate_input(client, username, password, message):
    # test invalid registration data
    response = client.post('/auth/register',
                           data={'username': username, 'password': password})
    assert message in response.data


def test_login(client, auth):
    # test login template rendered successfully
    assert client.get('auth/login').status_code == 200
    response = auth.login()
    # test redirection to index
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        # check user has been saved after login
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'),(
                         ('a', 'test', b'Incorrect username.'),
                         ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    # test invalid login data
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    with client:
        # test data deleted after logout
        auth.logout()
        assert 'user_id' not in session
