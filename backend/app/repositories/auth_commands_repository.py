"""
Module of Repository for auth
"""
from flask import current_app
from app.models import db, User
from app.constants.errors import ErrorMessages


class AuthCommandsRepository:
    """
    Repository for performing database operations related to authentication.
    """

    @staticmethod
    def get_user_by_username(username):
        """
        Retrieve a user by username.
        """
        try:
            return db.session.query(User).filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error(f"Error retrieving user by username: {e}")
            raise

    @staticmethod
    def create_user(username, password, role):
        """
        Create a new user and commit to the database.
        """
        try:
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            current_app.logger.error(f"Error creating user: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def user_exists(username):
        """
        Check if a user exists by username.
        """
        try:
            return db.session.query(User).filter_by(username=username).first() is not None
        except Exception as e:
            current_app.logger.error(f"Error checking if user exists: {e}")
            raise
