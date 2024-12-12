from flask import Flask
from flask_cors import CORS
import flask_monitoringdashboard as dashboard
from config import Config
from app.extensions import db, migrate
from app.register_blueprints import register_blueprints
from .logging import setup_logging
from app.db_commands import db_commands
from .config.swagger_config import setup_swagger
from .constants.config_strings import ConfigStrings

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    dashboard.config.init_from(file='../config.cfg')

    CORS(app, resources={r"/*": {"origins": ConfigStrings.CORS_ORIGINS}})

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    setup_swagger(app)

    setup_logging(app)

    db_commands(app)

    dashboard.bind(app)

    return app
