"""
Module intended to handle HTTP request connected with auth
"""

from flask import Blueprint, jsonify, request
from app.commands.auth_commands import LoginUserCommand, RegisterUserCommand
from app.constants.routes import Routes
from app.constants.infos import InfoMessages

bp = Blueprint(Routes.AUTH_BLUEPRINT, __name__)

@bp.route(Routes.REGISTER, methods=['POST'])
def register():
    """
    Register a new user and return a success message with the user ID.
    """
    data = request.get_json()
    user_id = RegisterUserCommand.execute(
        username=data['username'], 
        password=data['password'], 
        role='employee'
    )
    return jsonify({"message": InfoMessages.REGISTER_PASS, "user_id": user_id}), 201

@bp.route(Routes.LOGIN, methods=['POST'])
def login():
    """
    Authenticate a user and return a JWT token.
    """
    data = request.get_json()
    token = LoginUserCommand.execute(
        username=data['username'], 
        password=data['password']
    )
    return jsonify({"user": data['username'], "token": token}), 200
