from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # 🔥 1. validate input
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Missing fields"}), 400

    # 🔥 2. check duplicate email (ADD HERE)
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"msg": "Email already exists"}), 400

    # 🔥 3. hash password
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    # 🔥 4. get role
    role = data.get("role", "user")

    # 🔥 5. convert artist → pending
    if role == "artist":
        role = "pending_artist"

    # 🔥 6. create user
    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_pw,
        role=role
    )

    # 🔥 7. save
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "User created",
        "role": role
    })

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):

        # INCLUDE ROLE IN TOKEN
        token = create_access_token(
            identity={
                "id": user.id,
                "role": user.role
            }
        )
        return jsonify({
            "token": token,
            "role": user.role # send to frontend
        })

    return jsonify({"msg": "Invalid credentials"}), 401