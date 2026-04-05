import os

class Config:
  SECRET_KEY = "super-secret-key"
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  JWT_SECRET_KEY = "jwt-secret-key"

  CLOUDINARY_CLOUD_NAME =  "m-t-vi-t-group"
  CLOUDINARY_API_KEY = "289114531813425"
  CLOUDINARY_API_SECRET = "gp9eVWqKQkUT_YfmXgJ5YvlEQvA"