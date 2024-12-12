from flask import abort, current_app
from app.models import Room
from app.constants.errors import ErrorMessages

class GetRoomsQuery:
    @staticmethod
    def execute():
        """
        Fetch all rooms from the database.
        """
        try:
            rooms = Room.query.all()
            return [{"id": room.id, "name": room.name, "capacity": room.capacity} for room in rooms]
        except Exception as e:
            current_app.logger.error(f"Error fetching rooms: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)
