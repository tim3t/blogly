from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from traitlets import default

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

### MODELS BELOW ###

class User(db.Model):
    """Blogly User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, default="https://inceptum-stor.icons8.com/O73LU2odqyKc/ph_user-circle-fill%202.jpg")

class Post(db.Model):
    """User posts model."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey ('users.id'))

    by_user = db.relationship('User', backref='posts')


class Tag(db.Model):
    """Tag model, can add to posts"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary="posts_tags", backref="tags")

class PostTag(db.Model):
    """Join table for Posts and Tags"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

