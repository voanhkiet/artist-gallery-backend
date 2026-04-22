from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/pending", methods=["GET"])
@jwt_required()
def get_pending():
    current = get_jwt_identity()

    # 🔒 protect admin
    if current["role"] != "admin":
        return jsonify({"msg": "Forbidden"}), 403

    users = User.query.filter_by(role="pending_artist").all()

    return jsonify([
        {
            "id": u.id,
            "username": u.username,
            "email": u.email
        }
        for u in users
    ])

@admin_bp.route("/approve/<int:user_id>", methods=["POST"])
@jwt_required()
def approve(user_id):
    current = get_jwt_identity()

    if current["role"] != "admin":
        return jsonify({"msg": "Forbidden"}), 403

    user = User.query.get_or_404(user_id)

    user.role = "artist"
    db.session.commit()

    return jsonify({"msg": "Approved"})