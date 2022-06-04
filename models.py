from flask_sqlalchemy import SQLAlchemy

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

