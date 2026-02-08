import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name: str = None):
    load_dotenv()
    from config import config_map

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True, template_folder="templates", static_folder="static")
    app.config.from_object(config_map.get(config_name, config_map["development"]))

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .auth_routes import auth_bp
    from .post_routes import post_bp
    from .admin_routes import admin_bp
    from .utils.logging_conf import configure_logging

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(post_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    configure_logging(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
