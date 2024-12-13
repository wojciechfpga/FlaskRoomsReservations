"""
Module of Repository for retrieving room data from the database.
"""
from flask import abort, current_app
from app.models import Room
from app.constants.errors import ErrorMessages


class RoomsQueriesRepository:
    """
    Repository for retrieving room data from the database.
    """

    @staticmethod
    def get_all_rooms():
        """
        Fetch all rooms from the database.
        """
        try:
            return Room.query.all()
        except Exception as e:
            current_app.logger.error(f"Error fetching rooms: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)
