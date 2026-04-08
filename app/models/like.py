from app import db

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"))