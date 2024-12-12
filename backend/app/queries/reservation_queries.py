"""
Module with classed intended to made DB read operations
connected with reservations
"""

from flask import abort
from app.models import db, Reservation
from app.constants.errors import ErrorMessages

class ReservationQueries:
    """
    Class for handling reservation queries
    """
    
    @staticmethod
    def get_reservations(room_id=None, start_time=None, end_time=None):
        """
        Retrieving list of all reservations
        """
        try:
            query = db.session.query(Reservation).filter(Reservation.is_deleted.is_(False))

            if room_id:
                query = query.filter(Reservation.room_id == room_id)
            if start_time:
                query = query.filter(Reservation.end_time > start_time)
            if end_time:
                query = query.filter(Reservation.start_time < end_time)

            return query.order_by(Reservation.start_time).all()
        except Exception:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """
        Retrieve all reservations made by user
        """
        try:
            return db.session.query(Reservation).filter_by(user_id=user_id, is_deleted=False).all()
        except Exception:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Retrieve single reservation based on ID.
        """
        try:
            return db.session.query(Reservation).filter_by(id=reservation_id, is_deleted=False).first()
        except Exception:
            db.session.rollback()
            abort(500, description=ErrorMessages.SERVER_ERROR)

