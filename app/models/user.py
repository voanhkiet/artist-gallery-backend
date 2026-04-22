from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

    # NEW FIELD
    role = db.Column(db.String(20), default="user")

    # New
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.Text)


    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship("Image", backref="owner", lazy=True)