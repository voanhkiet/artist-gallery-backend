from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Image
from app import db
from app.utils.cloudinary import upload_image, delete_image

image_bp = Blueprint("images", __name__)

# Upload
@image_bp.route("/", methods=["POST"])
@jwt_required()
def upload():
    user_id = get_jwt_identity()

    file = request.files.get("image")
    title = request.form.get("title")
    description = request.form.get("description")

    # ✅ VALIDATION
    if not file or not title:
        return jsonify({"msg": "Missing image or title"}), 422

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
    images = Image.query.all()

    return jsonify([
        {
            "id": img.id,
            "title": img.title,
            "image_url": img.image_url,
            "user_id": img.user_id
        } for img in images
    ])


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