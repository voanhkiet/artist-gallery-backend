from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from flask_migrate import Migrate
from app.utils.cloudinary import init_cloudinary

app = create_app()

migrate = Migrate(app,db) 

with app.app_context():
    init_cloudinary(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)