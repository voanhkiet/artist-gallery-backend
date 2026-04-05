import cloudinary
import cloudinary.uploader
from flask import current_app

def init_cloudinary(app):
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"]
    )

def upload_image(file):
    result = cloudinary.uploader.upload(file)
    return result["secure_url"], result["public_id"]

def delete_image(public_id):
    cloudinary.uploader.destroy(public_id)