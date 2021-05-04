from helpers_tests import create_user, assert_flashes, assert_redirect, create_image

def test_if_not_user_to_visit(app, client):
    res = client.get("user/3")
    assert_flashes(client, "User doesn't exist")
    assert_redirect(res, "http://localhost/")

def test_user_has_no_images(app, client):
    user = create_user()
    res = client.get(f"user/{user.user_id}")
    if not user.images:
        assert_flashes(client, "User doesn't have any images")
        assert_redirect(res, "http://localhost/")

def test_not_public_image(app, client):
    user = create_user()
    image1 = create_image('image1', "s3://path-to-image-1", user.user_id)
    image2 = create_image('image2', "s3://path-to-image-2", user.user_id, True)
    res = res = client.get(f"user/{user.user_id}")
    print(res.data)
    assert b'<img src="s3://path-to-image-1" width="200" height="150">' not in res.data
    assert b'<img src="s3://path-to-image-2" width="200" height="150">' in res.data

def test_profile_success(app, client):
    user = create_user()
    image1 = create_image('image1', "s3://path-to-image-1", user.user_id, True)
    image2 = create_image('image2', "s3://path-to-image-2", user.user_id, True)
    res = res = client.get(f"user/{user.user_id}")
    assert res.status_code == 200