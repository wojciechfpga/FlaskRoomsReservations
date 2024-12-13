"""
Module of Repository for retrieving reservation data from the database.
"""
from flask import abort, current_app
from app.models import db, Reservation
from app.constants.errors import ErrorMessages


class ReservationQueriesRepository:
    @staticmethod
    def get_all_reservations():
        """
        Retrieve all non-deleted reservations.
        """
        try:
            return db.session.query(Reservation).filter(Reservation.is_deleted.is_(False))
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservations_by_filters(room_id=None, start_time=None, end_time=None):
        """
        Retrieve reservations filtered by room, start_time, and end_time.
        """
        try:
            query = ReservationQueriesRepository.get_all_reservations()
            
            if room_id:
                query = query.filter(Reservation.room_id == room_id)
            if start_time:
                query = query.filter(Reservation.end_time > start_time)
            if end_time:
                query = query.filter(Reservation.start_time < end_time)
            
            return query.order_by(Reservation.start_time).all()
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """
        Retrieve all reservations for a specific user.
        """
        try:
            return db.session.query(Reservation).filter_by(user_id=user_id, is_deleted=False).all()
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Retrieve a specific reservation by ID.
        """
        try:
            return db.session.query(Reservation).filter_by(id=reservation_id, is_deleted=False).first()
        except Exception as e:
            current_app.logger.error(f"{ErrorMessages.F_STRING_ERROR}: {e}")
            abort(500, description=ErrorMessages.SERVER_ERROR)
