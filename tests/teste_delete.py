from helpers_test import assert_redirect, create_image, create_user, create_logged_in_user, assert_not_logged_in_user, assert_flashes, create_file_data


def test_image_delete_failure(app, client):
    res = client.delete(f"/image/delete/9")
    assert_redirect(res, "http://localhost/")

def test_delete_user_doesnt_match(app, client):
    user = create_user()
    image = create_image('image1', "s3://path-to-image-1", user.user_id)
    create_logged_in_user(client, 1234)
    res = client.delete(f"/image/delete/{image.image_id}")
    
    assert_flashes(client, "Cannot modify other people's images")
    assert_redirect(res, "http://localhost/")

def test_delete_image_id_doesnt_exist(app, client):
    create_logged_in_user(client)
    res = client.delete(f"/image/delete/10")
    assert_flashes(client, "Image doesn't exist")
    assert_redirect(res, "http://localhost/")

def test_delete_image_success(app, client, mocker):
    # Creating no-op mocks for S3 / DB
    mocker.patch(
        "server.delete_from_s3", 
        return_value=True)
    mocker.patch(
        "server.delete_from_db", 
        return_value=True)

    user = create_user()
    image = create_image('image1', "s3://path-to-image-1", user.user_id)
    create_logged_in_user(client, user.user_id)
    res = client.delete(f"/image/delete/{image.image_id}")    
    assert_redirect(res, "http://localhost/my-images")

