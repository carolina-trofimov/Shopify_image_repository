from helpers_test import assert_redirect, create_image, create_user, create_logged_in_user, assert_not_logged_in_user, assert_flashes, create_file_data


def test_my_images_failure(app, client):
    res = client.put(f"/image/update/9")
    assert_redirect(res, "http://localhost/")

def test_publish_user_doesnt_match(app, client):
    user = create_user()
    image = create_image('image1', "s3://path-to-image-1", user.user_id)
    create_logged_in_user(client, 1234)

    res = client.put(f"/image/update/{image.image_id}", data={ "action" : 'publish'})
    
    assert_flashes(client, "Cannot modify other people's images")
    assert_redirect(res, "http://localhost/")

def test_image_id_doesnt_exist(app, client):
    create_logged_in_user(client)
    res = client.put(f"/image/update/", data={"action" : 'publish'})
    assert_flashes(client, "Image id not passed into the form")
    assert_redirect(res, "http://localhost/")

def test_image_id_doesnt_exist(app, client):
    create_logged_in_user(client)
    res = client.put(f"/image/update/10", data={"action" : 'publish'})
    assert_flashes(client, "Image doesn't exist")
    assert_redirect(res, "http://localhost/")

def test_publish_success(app, client):
    user = create_user()
    image = create_image('image1', "s3://path-to-image-1", user.user_id)
    create_logged_in_user(client, user.user_id)
    res = client.put(f"/image/update/{image.image_id}", data={ "action" : 'publish'})
    assert res.status_code == 200
    assert b'{"status":"published"}' in res.data

def test_unpublish_success(app, client):
    user = create_user()
    image = create_image('image1', "s3://path-to-image-1", user.user_id)
    create_logged_in_user(client, user.user_id)
    res = client.put(f"/image/update/{image.image_id}", data={ "action" : 'unpublish'})
    assert res.status_code == 200
    assert b'{"status":"unpublished"}' in res.data
