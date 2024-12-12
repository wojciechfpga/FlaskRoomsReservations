from flask_swagger_ui import get_swaggerui_blueprint
from app.constants.config_strings import ConfigStrings

def setup_swagger(app):
    swaggerui_blueprint = get_swaggerui_blueprint(
        ConfigStrings.SWAGGER_URL,
        ConfigStrings.API_URL,
        config={
            'app_name': "Conference Room Booking API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=ConfigStrings.SWAGGER_URL)
