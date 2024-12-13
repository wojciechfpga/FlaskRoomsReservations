"""
Commands connected with DB write operations on Reservations
"""
from flask import abort
from app.repositories.reservation_commands_repository import ReservationCommandsRepository
from app.services.room_service import is_time_conflict
from app.constants.errors import ErrorMessages

class CreateReservationCommand:
    @staticmethod
    def execute(room_id, user_id, start_time, end_time):
        """
        Creating new reservation without any conflict
        """
        if start_time >= end_time:
            abort(409, description=ErrorMessages.TIME_NOT_CORRECT)

        if is_time_conflict(room_id, start_time, end_time):
            abort(409, description=ErrorMessages.RESERVATION_CONFLICT)

        reservation = ReservationCommandsRepository.create_reservation(room_id, user_id, start_time, end_time)
        return reservation.id


class SoftDeleteReservationCommand:
    @staticmethod
    def execute(reservation_id):
        """
        Mark reservation as deleted (in DB - soft delete)
        """
        reservation = ReservationCommandsRepository.get_reservation_by_id(reservation_id)
        if not reservation or reservation.is_deleted:
            abort(409, description=ErrorMessages.RESERVATION_NOT_FOUND)

        ReservationCommandsRepository.soft_delete_reservation(reservation)


class UpdateReservationCommand:
    @staticmethod
    def execute(reservation_id, room_id, start_time, end_time):
        """
        Updating existing reservation without any conflict
        """
        if start_time >= end_time or is_time_conflict(room_id, start_time, end_time):
            abort(409, description=ErrorMessages.RESERVATION_CONFLICT)

        reservation = ReservationCommandsRepository.get_reservation_by_id(reservation_id)
        if not reservation or reservation.is_deleted:
            abort(409, description=ErrorMessages.RESERVATION_NOT_FOUND)

        updated_reservation = ReservationCommandsRepository.update_reservation(reservation, start_time, end_time)
        return {
            "id": updated_reservation.id,
            "start_time": updated_reservation.start_time,
            "end_time": updated_reservation.end_time,
            "room_id": updated_reservation.room_id,
            "room_name": updated_reservation.room.name,
        }


