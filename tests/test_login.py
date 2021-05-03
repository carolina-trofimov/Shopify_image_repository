import pytest
from model import db, User
from helpers_test import assert_flashes, assert_redirect

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200 


def test_login(app, client):
    res = client.get('/login')
    assert res.status_code == 200 

def test_handle_login_password_failure(app, client):
    res = client.post('/handle-login', data=dict(email="test@example.com", password=""), follow_redirects=False)
    assert_redirect(res,"http://localhost/login")
    assert_flashes(client, "Password is required for login")
    

def test_handle_login_email_failure(app, client):
    res = client.post('/handle-login', data=dict(email="", password="test_password"), follow_redirects=False)
    assert res.status_code == 302
    assert_redirect(res,"http://localhost/login")
    assert_flashes(client, "Email is required for login")


def test_handle_wrong_credentials_password(app, client):
    user = User(email="test@example.com", password="password")
    db.session.add(user)
    db.session.commit()
    res = client.post('/handle-login', data=dict(email="test@example.com", password="wrong_password"), follow_redirects=False)
    assert_flashes(client, "Incorrect Credentials")
    assert_redirect(res, "http://localhost/login")
    
def test_handle_wrong_credentials_email(app, client):
    user = User(email="test@example.com", password="password")
    db.session.add(user)
    db.session.commit()
    res = client.post('/handle-login', data=dict(email="wrongemail@example.com", password="password"), follow_redirects=False)
    assert_flashes(client, "Incorrect Credentials")
    assert_redirect(res, "http://localhost/register")

def test_handle_success_login(app, client):
    user = User(email="test@example.com", password="password")
    db.session.add(user)
    db.session.commit()
    res = client.post('/handle-login', data=dict(email="test@example.com", password="password"), follow_redirects=False)
    assert_flashes(client, "Login successful")
    assert_redirect(res, "http://localhost/upload")



