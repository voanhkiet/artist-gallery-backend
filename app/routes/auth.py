from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    role = data.get("role", "user")

    # artist must be approved first
    if role == "artist":
        role = "pending_artist"

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_pw,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):

        token = create_access_token(
            identity={
                "id": user.id,
                "role": user.role
            }
        )

        return jsonify({
            "token": token,
            "role": user.role
        })

    return jsonify({"msg": "Invalid credentials"}), 401