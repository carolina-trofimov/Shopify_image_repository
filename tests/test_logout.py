from helpers_tests import assert_redirect, assert_flashes, create_logged_in_user

def test_logout_failure(app, client):
    res = client.get("/logout")
    assert_redirect(res, "http://localhost/")

def test_logout_success(app, client):
    create_logged_in_user(client)
    res = client.get('/logout')
    assert_flashes(client, "Logout successful")
    assert_redirect(res, "http://localhost/")