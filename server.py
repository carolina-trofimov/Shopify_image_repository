from botocore.exceptions import ClientError
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from helpers import allowed_file, delete_from_s3, delete_from_db, login_required, save_image_to_s3, save_image_to_db
from flask_uploads import UploadSet, configure_uploads
from model import connect_to_db, db, User, Image
from os import environ
import io
import requests
from sqlalchemy import and_, update
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "123"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/register")
def register():
    """Show registration form."""

    return render_template("register.html")


@app.route("/handle-registration", methods=["POST"])
def register_user():
    """Register a new user."""

    new_email = request.form.get("email")
    new_password = request.form.get("password")

    if not new_email:
        flash("Email required for registration")
        return redirect("/register")
    if not new_password:
        flash("Password required for registration")
        return redirect("/register")

    user = User.query.filter_by(email=new_email).first()

    if user is None:
        user = User(email=new_email, password=new_password)
        db.session.add(user)
        db.session.commit()
        flash("New user created")
        session["logged_in_user"] = user.user_id
        return redirect("/upload")
    else:
        flash("This user already exists")
        return redirect("/login")


@app.route("/login")
def show_login_form():
    """Show login form."""

    return render_template("login.html")

@app.route("/handle-login", methods=["POST"])
def login():
    """Login user."""

    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        flash("Email is required for login")
        return redirect("/login")
    if not password:
        flash("Password is required for login")
        return redirect("/login")
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Incorrect Credentials")
        return redirect("/register")

    if password == user.password and email == user.email:
        flash("Login successful")
        session["logged_in_user"] = user.user_id
        return redirect("/upload")
    else:
        flash("Incorrect Credentials")
        return redirect("/login")


@app.route("/upload")
@login_required
def upload():
    """Show upload form."""
    print("render upload")
    return render_template('upload.html')

@app.route("/process-upload", methods=["POST"])
@login_required
def process_upload():
    """Upload file to S3 and add it to database."""
    
    # Processeses only 1 file (serially) (how do we do bulk?)
    user_id = session["logged_in_user"]

    if not user_id:
        flash("User Id not found")
        return redirect("/login")

    if 'file' not in request.files:
        flash("No file found")
        return redirect('/upload')

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect("/upload")

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename) 

        # Save image file to s3
        save_image_to_s3(filename, request.files['file'])

        # Save image path to db
        save_image_to_db(filename, user_id)

        flash("Image added")

    return redirect("/my-images")


@app.route("/my-images")
@login_required
def my_images():
    """Show images list."""
   
    user_id = session["logged_in_user"]
    images = Image.query.filter_by(user_id=user_id)

    return render_template("my_images.html", images=images)


@app.route("/image/update/<int:image_id>", methods=["PUT"])
@login_required
def publish(image_id):
    """Allow user to publish their own images"""

    if not image_id:
        flash("Image id not passed into the form")
        return redirect("/")

    # User will only be able to access their own images
    image = Image.query.get(image_id)

    if not image:
        flash("Image doesn't exist")
        return redirect("/")

    if image.user.user_id != session['logged_in_user']:
        flash("Cannot modify other people's images")
        return redirect("/")

    if request.form.get("action") == "publish":
        image.published = True
        db.session.add(image)
        db.session.commit()
        return jsonify({"status": "published"})

    else: 
        image.published = False
        db.session.add(image)
        db.session.commit()
        return jsonify({"status": "unpublished"})


@app.route("/image/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    """Allow user to delete an image"""

    image = Image.query.filter_by(image_id=image_id).first()
    user_id = session["logged_in_user"]

    if not image:
        flash("Image doesn't exist")
        return redirect("/")

    if image.user.user_id != session['logged_in_user']:
        flash("Cannot modify other people's images")
        return redirect("/")

    if user_id:
        image = Image.query.filter_by(image_id=image_id).one()
        delete_from_db(image)
        delete_from_s3(image.name)

        return redirect("/my-images")


@app.route("/users")
def all_users():
    """Show list of users to follow"""

    logged_user_id = session.get("logged_in_user")
    user = User.query.filter_by(user_id=logged_user_id).first()

    if user:
        users = User.query.filter(User.email != user.email).all()
    else:
        users = User.query.all()
    
    return render_template("users.html", users=users, loggedin_user=user)

#   if user logged in, user doesn't apper on user list
#   if user not logged in, see all users
#   if return 200

@app.route("/user/<int:user_id>")
def profile(user_id):
    """Show user profile with published podcasts"""                                   
    
    user_to_visit = User.query.get(user_id)

    if not user_to_visit:
        flash("User doesn't exist")
        print('no user')
        return redirect("/")

    images = Image.query.filter_by(user_id=user_to_visit.user_id, published=True).all()
    if not images:
        flash("User doesn't have any images")
        print('no images')
        return redirect("/")

    return render_template("profile.html", images=images, user_to_visit=user_to_visit) 
    

@app.route("/logout")
@login_required
def logout():
    """Logout user."""

    del session["logged_in_user"]
    flash("Logout successful")

    return redirect("/")
     

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///image_repository"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")