from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

    db.init_app(app)

    # Importar y registrar blueprints
    from app.routes.auth_routes import auth
    from app.routes.main_routes import main_bp

    app.register_blueprint(auth)
    app.register_blueprint(main_bp)

    return app
