from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix


db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    CORS(
        app,
        resources={r"/api/*": {"origins": "https://artist-gallery-alpha.vercel.app"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    # Models
    from app.models.user import User
    from app.models.image import Image
    from app.models.like import Like

    # Routes
    from app.routes.auth import auth_bp
    from app.routes.images import image_bp
    from app.routes.likes import like_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(image_bp, url_prefix="/api/images")
    app.register_blueprint(like_bp, url_prefix="/api/likes")

    return app