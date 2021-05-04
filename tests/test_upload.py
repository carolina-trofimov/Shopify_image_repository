from helpers_tests import create_logged_in_user, create_file_data, assert_redirect, assert_logged_in_user, assert_flashes


def test_upload_failure(app, client):
    res = client.get("/upload")
    assert_redirect(res, "http://localhost/")

def test_upload_success(app, client):
    create_logged_in_user(client)
    res = client.get("/upload")
    assert res.status_code == 200

def test_process_upload_success(app, client, mocker):
    # Creating no-op mocks for S3 / DB
    mocker.patch(
        "server.save_image_to_s3", 
        return_value=True)
    
    mocker.patch(
        "server.save_image_to_db", 
        return_value=True)

    create_logged_in_user(client)
    file = create_file_data()
    res = client.post('/process-upload', data=dict(file=file), follow_redirects=False, content_type="multipart/form-data") 
    assert_redirect(res, "http://localhost/my-images")


