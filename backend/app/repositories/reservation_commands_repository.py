"""
Module of Repository for writing reservation data from the database.
"""
from flask import abort
from app.models import db, Reservation
from app.constants.errors import ErrorMessages

class ReservationCommandsRepository:
    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Retrieve a reservation by its ID.
        """
        try:
            return db.session.query(Reservation).filter_by(id=reservation_id).first()
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def create_reservation(room_id, user_id, start_time, end_time):
        """
        Create a new reservation.
        """
        try:
            reservation = Reservation(
                room_id=room_id,
                user_id=user_id,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(reservation)
            db.session.commit()
            return reservation
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def update_reservation(reservation, start_time, end_time):
        """
        Update an existing reservation.
        """
        try:
            reservation.start_time = start_time
            reservation.end_time = end_time
            db.session.commit()
            return reservation
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def soft_delete_reservation(reservation):
        """
        Mark a reservation as deleted.
        """
        try:
            reservation.is_deleted = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)
