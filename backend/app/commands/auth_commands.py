"""
This module is intended to provide functions thats executes DB commands
connected with auth operations
"""

import datetime
import jwt
from flask import current_app, abort
from app.repositories.auth_commands_repository import AuthCommandsRepository
from app.constants.errors import ErrorMessages


class RegisterUserCommand:
    """
    Command to register a new user.
    """

    @staticmethod
    def execute(username, password, role):
        """
        Register a new user with a hashed password.
        """
        if not username or not password:
            abort(400, description=ErrorMessages.INVALID_AUTH)

        
        if AuthCommandsRepository.user_exists(username):
            abort(409, description=ErrorMessages.USER_ALREADY_EXISTS)

        user = AuthCommandsRepository.create_user(username, password, role)

        return user.id



class LoginUserCommand:
    """
    Command to log in a user and generate a JWT token.
    """

    @staticmethod
    def execute(username, password):
        """
        Authenticate a user and generate a JWT token if credentials are valid.
        """
        user = AuthCommandsRepository.get_user_by_username(username)
        if not user or not user.check_password(password):
            abort(403, description=ErrorMessages.INVALID_AUTH)

        token = jwt.encode(
            {
                "user_id": user.id,
                "role": user.role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return token


