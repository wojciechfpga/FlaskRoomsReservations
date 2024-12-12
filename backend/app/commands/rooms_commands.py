from flask import abort, current_app
from app.models import Room,db
from app.constants.errors import ErrorMessages
from app.constants.infos import InfoMessages
class CreateRoomCommand:
    @staticmethod
    def execute(name, capacity):
        """
        Create a new room and save to the database, ensuring no room with the same name exists.
        """
        try:
            existing_room = Room.query.filter_by(name=name).first()
            if existing_room:
                raise ValueError(ErrorMessages.ROOM_EXIST)

            room = Room(name=name, capacity=capacity)
            db.session.add(room)
            db.session.commit()
            return room.id
        
        except ValueError as ve:
            current_app.logger.info(ve)
            abort(409, description=str(ve))
        
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR) 
        

class UpdateRoomCommand:
    @staticmethod
    def execute(room_id, name=None, capacity=None, is_active=None):
        """
        Update a room's details based on the given parameters.
        """
        try:
            room = Room.query.get(room_id)
            if not room:
                raise ValueError(ErrorMessages.ROOM_NOT_FOUND)

            if name is not None:
                if Room.query.filter(Room.name == name, Room.id != room_id).first():
                    raise ValueError(ErrorMessages.ROOM_EXIST)
                room.name = name

            if capacity is not None:
                room.capacity = capacity
            
            if is_active is not None:
                room.is_active = is_active

            db.session.commit()

        except ValueError as ve:
            current_app.logger.info(ve)
            abort(400, description=str(ve))

        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

class DeleteRoomCommand:
    @staticmethod
    def execute(room_id):
        """
        Delete a room with the given room_id.
        """
        try:
            room = Room.query.get(room_id)
            if not room:
                raise ValueError(ErrorMessages.ROOM_NOT_FOUND)

            db.session.delete(room)
            db.session.commit()

            return {"message": InfoMessages.ROOM_OPERATION_PASS}

        except ValueError as ve:
            current_app.logger.info(ve)
            abort(404, description=str(ve))

        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

