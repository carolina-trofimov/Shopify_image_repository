import pytest
from model import db, User
from helpers_test import assert_flashes, assert_logged_in_user, assert_redirect

def test_register(app, client):
    res = client.get('/register')
    assert res.status_code == 200 

def test_handle_register_password_failure(app, client):
    res = client.post('/handle-registration', data=dict(email="test@example.com", password=""), follow_redirects=False)
    assert_redirect(res,"http://localhost/register")
    assert_flashes(client, "Password required for registration")

def test_handle_register_email_failure(app, client):
    res = client.post('/handle-registration', data=dict(email="", password="password"), follow_redirects=False)
    assert_redirect(res, "http://localhost/register")
    assert_flashes(client, "Email required for registration")

def test_handle_user_already_exists(app, client):
    user = User(email="test@example.com", password="password")
    db.session.add(user)
    db.session.commit()
    res = client.post('/handle-registration', data=dict(email="test@example.com", password="password"), follow_redirects=False)
    assert_flashes(client, "This user already exists")
    assert_redirect(res,"http://localhost/login")

def test_handle_registration_success(app, client):
    res = client.post('/handle-registration', data=dict(email="new_user@example.com", password="password"), follow_redirects=False)
    User.query.filter_by(email="new_user@example.com").first()
    users = User.query.all()
    assert_flashes(client, "New user created")
    assert len(users) == 1
    assert_logged_in_user(client, users[0].user_id)
    assert_redirect(res,"http://localhost/upload")