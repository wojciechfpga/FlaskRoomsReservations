def register_blueprints(app):
    from app.blueprints.room_blueprint import bp as room_bp
    from app.blueprints.reservation_blueprint import bp as reservation_bp
    from app.blueprints.auth_blueprint import bp as auth_bp

    app.register_blueprint(room_bp, url_prefix='/api')
    app.register_blueprint(reservation_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
