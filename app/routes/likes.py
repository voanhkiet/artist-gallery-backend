from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.like import Like

like_bp = Blueprint("likes", __name__)

@like_bp.route("/toggle/<int:image_id>", methods=["POST"])
@jwt_required()
def toggle_like(image_id):
    user_id = get_jwt_identity()

    existing = Like.query.filter_by(user_id=user_id, image_id=image_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"liked": False})

    new_like = Like(user_id=user_id, image_id=image_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"liked": True})


@like_bp.route("/count/<int:image_id>", methods=["GET"])
def like_count(image_id):
    count = Like.query.filter_by(image_id=image_id).count()
    return jsonify({"count": count})