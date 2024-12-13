"""
Module with classes intended to execute DB write operations
connected with rooms
"""

from flask import abort
from app.repositories.room_repository import RoomRepository
from app.constants.errors import ErrorMessages
from app.constants.infos import InfoMessages

class CreateRoomCommand:
    @staticmethod
    def execute(name, capacity):
        """
        Create a new room and save to the database, ensuring no room with the same name exists.
        """
        if RoomRepository.get_room_by_name(name):
            abort(409, description=ErrorMessages.ROOM_EXIST)

        room = RoomRepository.create_room(name, capacity)
        return room.id


class UpdateRoomCommand:
    @staticmethod
    def execute(room_id, name=None, capacity=None, is_active=None):
        """
        Update a room's details based on the given parameters.
        """
        room = RoomRepository.get_room_by_id(room_id)
        if not room:
            abort(404, description=ErrorMessages.ROOM_NOT_FOUND)

        if name and RoomRepository.check_room_name_conflict(name, room_id):
            abort(409, description=ErrorMessages.ROOM_EXIST)

        if name:
            room.name = name
        if capacity:
            room.capacity = capacity
        if is_active is not None:
            room.is_active = is_active

        RoomRepository.update_room(room)


class DeleteRoomCommand:
    @staticmethod
    def execute(room_id):
        """
        Delete a room with the given room_id.
        """
        room = RoomRepository.get_room_by_id(room_id)
        if not room:
            abort(404, description=ErrorMessages.ROOM_NOT_FOUND)

        RoomRepository.delete_room(room)
        return {"message": InfoMessages.ROOM_OPERATION_PASS}

