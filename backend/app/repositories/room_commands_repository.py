"""
Module of Repository for writing room data from the database.
"""
from flask import abort, current_app
from app.models import Room, db
from app.constants.errors import ErrorMessages

class RoomCommandsRepository:
    @staticmethod
    def get_room_by_id(room_id):
        """
        Retrieve a room by its ID.
        """
        try:
            return Room.query.get(room_id)
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_room_by_name(name):
        """
        Retrieve a room by its name.
        """
        try:
            return Room.query.filter_by(name=name).first()
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def check_room_name_conflict(name, room_id=None):
        """
        Check if a room with the given name exists, excluding a specific room_id.
        """
        try:
            query = Room.query.filter(Room.name == name)
            if room_id:
                query = query.filter(Room.id != room_id)
            return query.first()
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def create_room(name, capacity):
        """
        Create and save a new room.
        """
        try:
            room = Room(name=name, capacity=capacity)
            db.session.add(room)
            db.session.commit()
            return room
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def update_room(room):
        """
        Save updates to an existing room.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def delete_room(room):
        """
        Delete a room.
        """
        try:
            db.session.delete(room)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)
