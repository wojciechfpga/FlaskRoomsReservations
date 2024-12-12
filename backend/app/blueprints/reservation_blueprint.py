"""
Module intended to handle HTTP request connected with reservations
"""

import datetime
from flask import Blueprint, jsonify, request, current_app
from app.commands.reservation_commands import CreateReservationCommand, SoftDeleteReservationCommand, UpdateReservationCommand
from app.queries.reservation_queries import ReservationQueries
from app.auth.middleware import authorization_jwt
from app.constants.logs import LogMessages
from app.constants.routes import Routes
from app.constants.infos import InfoMessages
from app.constants.roles import Roles

bp = Blueprint(Routes.RESERVATION_BLUEPRINT, __name__)

@bp.route(Routes.RESERVATIONS, methods=['POST'])
@authorization_jwt(Roles.EMPLOYEE, Roles.ADMIN)
def create_reservation(user_id):
    """
    Create Reservation
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    data = request.get_json()
    try:
        reservation_id = CreateReservationCommand.execute(
            room_id=data['room_id'],
            user_id=user_id,
            start_time=datetime.datetime.fromisoformat(data['start_time']),
            end_time=datetime.datetime.fromisoformat(data['end_time'])
        )
        return jsonify({"message": InfoMessages.RESERVATION_OPERATION_PASS, "id": reservation_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route(f'/{Routes.RESERVATIONS}/<int:reservation_id>', methods=['DELETE'])
@authorization_jwt(Roles.EMPLOYEE, Roles.ADMIN)
def delete_reservation(user_id, reservation_id):
    """
    Soft delete of reservation
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    SoftDeleteReservationCommand.execute(reservation_id)
    return jsonify({"message": InfoMessages.RESERVATION_OPERATION_PASS}), 200


@bp.route(f'/{Routes.RESERVATIONS}/all', methods=['GET'])
@authorization_jwt(Roles.ADMIN)
def get_all_reservations(user_id):
    """
    All reservations - admins only
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    reservations = ReservationQueries.get_reservations()
    return jsonify([{
        "id": r.id,
        "room_id": r.room_id,
        "user_id": r.user_id,
        "start_time": r.start_time.isoformat(),
        "end_time": r.end_time.isoformat()
    } for r in reservations])


@bp.route(f'/{Routes.RESERVATIONS}/my', methods=['GET'])
@authorization_jwt(Roles.EMPLOYEE, Roles.ADMIN)
def get_my_reservations(user_id):
    """
    All reservations of user
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    reservations = ReservationQueries.get_reservations_by_user_id(user_id)
    return jsonify([{
        "id": r.id,
        "room_id": r.room_id,
        "room_name": r.room.name,
        "start_time": r.start_time.isoformat(),
        "end_time": r.end_time.isoformat()
    } for r in reservations])


@bp.route(f'/{Routes.RESERVATIONS}/<int:reservation_id>', methods=['PATCH'])
@authorization_jwt(Roles.EMPLOYEE, Roles.ADMIN)
def update_reservation(user_id, reservation_id):
    """
    Update reservation of user
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    data = request.get_json()
    reservation = UpdateReservationCommand.execute(reservation_id, data['room_id'], data['start_time'], data['end_time'])
    return jsonify({
        "id": reservation["id"],
        "start_time": reservation["start_time"],
        "end_time": reservation["end_time"],
        "room_id": reservation["room_id"],
        "room_name": reservation["room_name"],
    }), 200
