from app import db
from app.models import Room 

def initialize_database():
    """
    Initialization of DB
    """
    db.drop_all()
    db.create_all()

