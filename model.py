from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    """Data model for an user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)
    

    def __repr__(self):
        """Return a human-readable representation of an User."""
        return f"< email{self.email}>"

class Image(db.Model):
    """Data model for an image."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True,)
    name = db.Column(db.String(100), nullable=False,)
    s3_path = db.Column(db.String(300), nullable=False,)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'),
                         nullable=False,
                         )
    user = db.relationship('User', backref='images')
    published = db.Column(db.Boolean, nullable=False, unique=False, default=False)

    def __repr__(self):
        """Return a human-readable representation of an Image."""
        return f"<image_id={self.image_id} name={self.name}>"

def connect_to_db(app):
    """Connect the database to our Flask app."""
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///image_repository"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    connect_to_db(app)
    db.create_all()
