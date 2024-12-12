def db_commands(app):
    @app.cli.command("init-db")
    def init_db():
        with app.app_context(): 
            from app.db import initialize_database
            initialize_database()
