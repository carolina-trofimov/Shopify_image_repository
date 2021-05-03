from boto.s3.connection import S3Connection, Bucket, Key
from constants import ALLOWED_EXTENSIONS, s3_client, s3, bucket
from flask import Flask, flash, session, redirect
from functools import wraps
from os import environ
from model import Image, User, db, connect_to_db

aws_secret_access_key = environ.get("AWSSecretKey")
aws_access_key_id = environ.get("AWSAccessKeyId")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('logged_in_user', None)
        if user:
            return f(*args, **kwargs)
        else:
            # Add flash message
            return redirect("/")
    return decorated_function


def allowed_file(filename):
    """Check if file is in the correct extension mp3."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image_to_s3(filename, file):
    """Save image to S3 bucket"""
 
    s3_path = f"s3://shopifyimagerepository/{filename}"
    
    s3_client.put_object(Body=file,
                      Bucket="shopifyimagerepository",
                      Key=filename,
                      ACL="public-read")


def save_image_to_db(filename, user_id):
    """Save image to databade"""

    s3_path = f"https://shopifyimagerepository.s3-us-west-1.amazonaws.com/{filename}"

    image = Image(user_id=user_id, name=filename, s3_path=s3_path)
    db.session.add(image)
    db.session.commit()
    return image.image_id


def delete_from_s3(image_name):
    """Delete image from S3 bucket"""
    conn = S3Connection(aws_access_key_id, aws_secret_access_key)
    bucket = Bucket(conn, "shopifyimagerepository")
    k = Key(bucket)
    k.key = image_name
    bucket.delete_key(k)


def delete_from_db(image):
    """Delete image from database"""
    db.session.delete(image)
    db.session.commit()
