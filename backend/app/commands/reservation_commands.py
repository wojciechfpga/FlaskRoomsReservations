from flask import abort
from app.models import db, Reservation
from app.services.room_service import is_time_conflict
from app.constants.errors import ErrorMessages
class CreateReservationCommand:
    @staticmethod
    def execute(room_id,user_id,start_time, end_time):
        """
        Creating new reservation without any conflict
        """
        try:
            if start_time >= end_time:
                raise ValueError(ErrorMessages.TIME_NOT_CORRECT)

            if is_time_conflict(room_id, start_time, end_time):
                raise ValueError(ErrorMessages.RESERVATION_CONFLICT)

            reservation = Reservation(
                room_id=room_id,
                user_id=user_id,  
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(reservation)
            db.session.commit()
            return reservation.id
        except ValueError as e:
            db.session.rollback()
            abort(409, description=str(e))
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.Server)


class SoftDeleteReservationCommand:
    @staticmethod
    def execute(reservation_id):
        """
        Mark reservation as deleted (in DB - soft delete)
        """
        try:
            reservation = db.session.query(Reservation).filter_by(id=reservation_id).first()
            if not reservation or reservation.is_deleted:
                raise ValueError(ErrorMessages.TIME_NOT_CORRECT)

            reservation.is_deleted = True
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            abort(409, description=str(e))
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)


class UpdateReservationCommand:
    @staticmethod
    def execute(id, room_id, start_time, end_time):
        """
        Updating existing reservation without any conflict
        """
        try:
            if start_time >= end_time or is_time_conflict(room_id, start_time, end_time):
                raise ValueError(ErrorMessages.RESERVATION_CONFLICT)
                
            reservation = db.session.query(Reservation).filter_by(id=id).one()
            reservation.start_time = start_time
            reservation.end_time = end_time

            db.session.commit()
            return {
                "id": reservation.id,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "room_id": reservation.room_id,
                "room_name": reservation.room.name,
            }
        except ValueError as e:
            abort(409, description=str(e))
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

