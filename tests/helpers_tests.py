from constants_tests import SMALLEST_JPEG_B64
import io
import werkzeug
import base64
from model import db, User, Image

def assert_flashes(client, expected_message, expected_category='message'):
        with client.session_transaction() as session:
            try:
                category, message = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            assert expected_message in message
            assert expected_category == category

def assert_logged_in_user(client, expected_user_id=1):
    with client.session_transaction() as session:
        assert session['logged_in_user'] == expected_user_id

def assert_not_logged_in_user(client, user_id=123, expected_user_id=321):
    with client.session_transaction() as session:
        assert user_id != expected_user_id

def assert_redirect(response, expected_location):
    assert response.status_code == 302
    assert response.headers['Location'] == expected_location

def create_logged_in_user(client, expected_user_id=123):
        with client.session_transaction() as session:
            session['logged_in_user'] = expected_user_id

def create_user(email="test@example.com", password="password"):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def create_image(name, path, for_user):
    image = Image(
        name = name,
        s3_path = path,
        user_id = for_user
    )
    db.session.add(image)
    db.session.commit()
    return image


def create_file_data(data=SMALLEST_JPEG_B64, expected_filename="my_image.jpg", expected_content_type="image/jpg"):
    file = werkzeug.datastructures.FileStorage(
                stream=io.BytesIO(base64.b64decode(data)),
                filename=expected_filename,
                content_type=expected_content_type,
            )
    return file