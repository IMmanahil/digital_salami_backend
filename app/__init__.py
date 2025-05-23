# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import Config
import os
from app.utils.loggers import setup_logger  # Custom logger setup
from app.errors import register_error_handlers
# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Setup centralized app logger
logger = setup_logger("DigitalSalami")
logger.info("🚀 Logging initialized for Digital Salami backend")

def create_app():
    app = Flask(__name__)

    # Load all configuration from config.py
    app.config.from_object(Config)

    # Initialize extensions with app instance
    db.init_app(app)
    migrate.init_app(app, db)

    logger.info(f"✅ Connected to DB: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Import models (important for migrations to detect them)
    from app import models
    from app.models import transaction

    # Register Blueprints (routes)
    from app.routes.auth_routes import auth_bp
    from app.routes.transaction_routes import transaction_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transaction_bp, url_prefix='/api/transaction')
    register_error_handlers(app)

    return app
