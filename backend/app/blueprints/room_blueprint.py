"""
Module intended to handle HTTP request connected with rooms
"""

from flask import Blueprint, jsonify, request, current_app
from app.constants.logs import LogMessages
from app.commands.rooms_commands import CreateRoomCommand, DeleteRoomCommand, UpdateRoomCommand
from app.queries.rooms_queries import GetRoomsQuery
from app.auth.middleware import authorization_jwt
from app.constants.routes import Routes
from app.constants.infos import InfoMessages
from app.constants.roles import Roles

bp = Blueprint(Routes.ROOM_BLUEPRINT, __name__)

@bp.route(Routes.ROOMS, methods=['GET'])
def get_rooms():
    """
    Get rooms
    """
    rooms = GetRoomsQuery.execute()
    return jsonify(rooms)

@bp.route(Routes.ROOMS, methods=['POST'])
@authorization_jwt(Roles.ADMIN)
def create_room(user_id):
    """
    Create room
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    data = request.get_json()
    room_id = CreateRoomCommand.execute(name=data['name'], capacity=data['capacity'])
    current_app.logger.info(LogMessages.ROOM_CREATED.format(room_name=data['name']))
    return jsonify({"message": InfoMessages.ROOM_OPERATION_PASS, "id": room_id}), 201

@bp.route(f'/{Routes.ROOMS}/<int:room_id>', methods=['PUT'])
@authorization_jwt(Roles.ADMIN)
def update_room(user_id, room_id):
    """
    Update of room
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    data = request.get_json()
    UpdateRoomCommand.execute(
        room_id=room_id,
        name=data.get('name'),
        capacity=data.get('capacity'),
        is_active=data.get('is_active')
    )
    return jsonify({"message": InfoMessages.ROOM_OPERATION_PASS}), 200

@bp.route(f'/{Routes.ROOMS}/<int:room_id>', methods=['DELETE'])
@authorization_jwt(Roles.ADMIN)
def delete_room(user_id, room_id):
    """
    Delete of room
    """
    current_app.logger.info(LogMessages.USER_ENTERED_INTO.format(user_id=user_id, endpoint_name=request.endpoint))
    DeleteRoomCommand.execute(room_id=room_id)
    return jsonify({"message": InfoMessages.ROOM_OPERATION_PASS}), 200
