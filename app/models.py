from app import db
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(200))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  images = db.relationship("Image", backref="owner", lazy=True)


class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200))
  description = db.Column(db.Text)
  image_url = db.Column(db.String(300))
  public_id = db.Column(db.String(200))

  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)