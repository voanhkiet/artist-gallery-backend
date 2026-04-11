from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Image, Like, User
from app import db
from app.utils.cloudinary import upload_image, delete_image

image_bp = Blueprint("images", __name__)

# Upload
@image_bp.route("/", methods=["POST"])
def upload():
    print("CONTENT TYPE:", request.content_type)
    print("FILES:", request.files)
    print("FORM:", request.form)

    file = request.files.get("image")
    title = request.form.get("title")
    description = request.form.get("description")

    if not file or not title:
        return jsonify({"msg": "Missing image or title"}), 422

    # 🔥 FIX JWT
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    from flask_jwt_extended.exceptions import JWTExtendedException

    try:
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())
        print("USER ID:", user_id)
    except JWTExtendedException as e:
        print("JWT ERROR:", str(e))
        return jsonify({"msg": "JWT invalid"}), 401

    if not user_id:
        return jsonify({"msg": "Invalid token"}), 401

    image_url, public_id = upload_image(file)

    image = Image(
        title=title,
        description=description,
        image_url=image_url,
        public_id=public_id,
        user_id=user_id
    )

    db.session.add(image)
    db.session.commit()

    return jsonify({"msg": "Image uploaded"})


# Get all (public)
@image_bp.route("/", methods=["GET"])
def get_images():
    from flask_jwt_extended import verify_jwt_in_request
    from flask_jwt_extended.exceptions import JWTExtendedException

    user_id = None

    # 🔥 try get user (optional login)
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except JWTExtendedException:
        pass

    images = Image.query.all()

    result = []

    for img in images:
        # 👍 count likes
        likes_count = Like.query.filter_by(image_id=img.id).count()

        # ❤️ check if current user liked
        is_liked = False
        if user_id:
            is_liked = Like.query.filter_by(
                user_id=user_id,
                image_id=img.id
            ).first() is not None

        result.append({
            "id": img.id,
            "title": img.title,
            "description": img.description,
            "image_url": img.image_url,
            "created_at": img.created_at.isoformat() if img.created_at else None,
            "user": img.owner.username if img.owner else "Unknown",

            # 🔥 NEW FIELDS
            "likes_count": likes_count,
            "is_liked": is_liked
        })

    return jsonify(result)


# Update
@image_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    user_id = get_jwt_identity()
    image = Image.query.get_or_404(id)

    if image.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.json
    image.title = data.get("title", image.title)
    image.description = data.get("description", image.description)

    db.session.commit()

    return jsonify({"msg": "Updated"})


# Delete
@image_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    user_id = get_jwt_identity()
    image = Image.query.get_or_404(id)

    if image.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    delete_image(image.public_id)

    db.session.delete(image)
    db.session.commit()

    return jsonify({"msg": "Deleted"})

@image_bp.route("/user/<username>", methods=["GET"])
def get_user_images(username):
    images = Image.query.join(User).filter(User.username == username).all()

    result = []
    for img in images:
        result.append({
            "id": img.id,
            "title": img.title,
            "image_url": img.image_url,
            "created_at": img.created_at.isoformat() if img.created_at else None,
            "user": img.owner.username if img.owner else "Unknown"
        })

    return jsonify(result)

@image_bp.route("/user/profile/<username>", methods=["GET"])
def get_user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    return jsonify({
        "username": user.username,
        "avatar_url": user.avatar_url,
        "bio": user.bio
    })

@image_bp.route("/user/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    data = request.json

    user.bio = data.get("bio", user.bio)
    user.avatar_url = data.get("avatar_url", user.avatar_url)

    db.session.commit()

    return jsonify({"msg": "Profile updated"})