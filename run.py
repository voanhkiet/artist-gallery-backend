from app import create_app, db
from app.utils.cloudinary import init_cloudinary

app = create_app()

with app.app_context():
    db.create_all()
    init_cloudinary(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)