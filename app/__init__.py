import json
from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    with app.app_context():
        from app.models import models

        db.create_all()

    # Register blueprints here
    from app.routes import bp as main_bp

    app.register_blueprint(main_bp)

    return app
