from helpers_tests import create_user, create_logged_in_user


def test_logged_in_user_not_in_list(app, client):
    user = create_user()
    logged_in_user = create_logged_in_user(client, user.user_id)
    user2 = create_user("test2@example.com", "password2")
    user3 = create_user("test3@example.com", "password3")
    res = client.get("/users")
    assert b'<a href="/user/1">test1@example.com</a>' not in res.data
    assert b'<a href="/user/2">test2@example.com</a>' in res.data
    assert b'<a href="/user/3">test3@example.com</a>' in res.data

def test_not_logged_in_user(app, client):
    user1 = create_user("test1@example.com", "password1")
    user2 = create_user("test2@example.com", "password2")
    res = client.get("/users")
    assert b'<a href="/user/1">test1@example.com</a>' in res.data
    assert b'<a href="/user/2">test2@example.com</a>' in res.data
    assert res.status_code == 200