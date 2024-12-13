"""
Module with classes intended to perform DB read operations
connected with rooms
"""

from flask import abort
from app.repositories.rooms_queries_repository import RoomsQueriesRepository
from app.constants.errors import ErrorMessages


class GetRoomsQuery:
    """
    Class with method to get all rooms.
    """

    @staticmethod
    def execute():
        """
        Fetch all rooms and return as a list of dictionaries.
        """
        try:
            rooms = RoomsQueriesRepository.get_all_rooms()
            return [
                {"id": room.id, "name": room.name, "capacity": room.capacity}
                for room in rooms
            ]
        except Exception:
            abort(500, description=ErrorMessages.SERVER_ERROR)

