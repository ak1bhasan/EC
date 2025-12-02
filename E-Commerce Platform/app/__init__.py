from flask import Flask
import os
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_object="config.DevConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get(int(user_id))

    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.products import products_bp
    from app.blueprints.cart import cart_bp
    from app.blueprints.orders import orders_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(products_bp, url_prefix="/")
    app.register_blueprint(cart_bp, url_prefix="/")
    app.register_blueprint(orders_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
