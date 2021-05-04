from helpers_tests import create_user, create_image, create_logged_in_user, create_file_data, assert_redirect, assert_logged_in_user, assert_flashes
from model import Image, User

def test_my_images_failure(app, client):
    res = client.get("/my-images")
    assert_redirect(res, "http://localhost/")


def test_my_images_success_empty(app, client):
    create_logged_in_user(client)
    res = client.get("/my-images")
    assert res.status_code == 200


def test_my_images_success_all(app, client):
    # Have a user
    user = create_user()
    # User is logged in user
    print(user.user_id)
    create_logged_in_user(client, user.user_id)
    # User has images
    image1 = create_image('image1', 's3://image-path-1', user.user_id)
    image2 = create_image('image2', 's3://image-path-2', user.user_id)
    res = client.get("/my-images")
    assert res.status_code == 200
    assert b'image1' in res.data
    assert b's3://image-path-1' in res.data
    assert b'image2' in res.data
    assert b's3://image-path-2' in res.data

def test_how_many_images_empty(app, client):
    user = create_user()
    create_logged_in_user(client, 12345)
    image1 = create_image('image1', 's3://image-path-1', user.user_id)
    image2 = create_image('image2', 's3://image-path-2', user.user_id)
    res = client.get("/my-images")
    assert res.status_code == 200
    assert b'image1' not in res.data
    assert b's3://image-path-1' not in res.data
