from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from pymongo import MongoClient
from flask_cors import CORS 
import logging
from config import Config
import flask_monitoringdashboard as dashboard
from app.constants.config_strings import ConfigStrings

db = SQLAlchemy()
migrate = Migrate()

class MongoHandler(logging.Handler):
    """Custom logging handler to write logs to MongoDB."""
    def __init__(self, mongo_uri, database, collection):
        super().__init__()
        client = MongoClient(mongo_uri)
        self.collection = client[database][collection]

    def emit(self, record):
        log_entry = self.format(record)
        self.collection.insert_one({
            "log": log_entry,
            "level": record.levelname,
            "message": record.msg,
            "time": record.asctime,
        })

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    dashboard.config.init_from(file='../config.cfg')

    CORS(app, resources={r"/*": {"origins": ConfigStrings.CORS_ORIGINS}})

    db.init_app(app)

    from app.blueprints.room_blueprint import bp as room_bp
    from app.blueprints.reservation_blueprint import bp as reservation_bp
    from app.blueprints.auth_blueprint import bp as auth_bp
    app.register_blueprint(room_bp, url_prefix='/api')
    app.register_blueprint(reservation_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    swaggerui_blueprint = get_swaggerui_blueprint(
        ConfigStrings.SWAGGER_URL,
        ConfigStrings.API_URL,
        config={
            'app_name': "Conference Room Booking API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=ConfigStrings.SWAGGER_URL)

    @app.cli.command("init-db")
    def init_db():
        with app.app_context(): 
            from app.db import initialize_database
            initialize_database()

    mongo_handler = MongoHandler(ConfigStrings.MONGO_URI, ConfigStrings.LOG_DATABASE, ConfigStrings.LOG_COLLECTION)
    mongo_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    mongo_handler.setFormatter(formatter)

    app.logger.addHandler(mongo_handler)

    dashboard.bind(app)
    return app
