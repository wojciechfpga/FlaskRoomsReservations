"""
Module with classed intended to made DB read operations
connected with reservations
"""

from flask import abort
from app.repositories.reservation_queries_repository import ReservationQueriesRepository
from app.constants.errors import ErrorMessages


class ReservationQueries:
    """
    Class for handling reservation queries
    """

    @staticmethod
    def get_reservations(room_id=None, start_time=None, end_time=None):
        """
        Retrieve a list of all reservations based on optional filters.
        """
        try:
            return ReservationQueriesRepository.get_reservations_by_filters(room_id, start_time, end_time)
        except Exception:
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """
        Retrieve all reservations made by a specific user.
        """
        try:
            return ReservationQueriesRepository.get_reservations_by_user_id(user_id)
        except Exception:
            abort(500, description=ErrorMessages.SERVER_ERROR)

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """
        Retrieve a single reservation based on its ID.
        """
        reservation = ReservationQueriesRepository.get_reservation_by_id(reservation_id)
        if not reservation:
            abort(404, description=ErrorMessages.RESERVATION_NOT_FOUND)
        return reservation


