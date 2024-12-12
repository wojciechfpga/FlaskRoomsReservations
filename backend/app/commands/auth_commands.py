from app.models import db, User
import jwt
import datetime
from flask import current_app,abort
from app.models import User
from app.constants.errors import ErrorMessages
class RegisterUserCommand:
    @staticmethod
    def execute(username, password, role):
        """
        Register a new user with a hashed password.
        """
        try:
            if not username or not password:
                raise ValueError(ErrorMessages.INVALID_AUTH)

            existing_user = db.session.query(User).filter_by(username=username).first()
            if existing_user:
                raise ValueError(ErrorMessages.USER_ALREADY_EXISTS)

            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            return user.id
        except ValueError as ve:
            current_app.logger.info(ve)
            abort(409, description=str(ve)) 
        except Exception as e:
            current_app.logger.info(e)
            abort(500, description=ErrorMessages.SERVER_ERROR) 


class LoginUserCommand:
    @staticmethod
    def execute(username, password):
        """
        Authenticate user and generate JWT token if credentials are valid.
        """
        try:
            user = db.session.query(User).filter_by(username=username).first()

            if not user or not user.check_password(password):
                raise ValueError(ErrorMessages.INVALID_AUTH)

            token = jwt.encode(
                {"user_id": user.id, "role": user.role, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return token
        except ValueError as ve:
            current_app.logger.info(ve)
            abort(403, description=str(ve)) 
        except Exception as e:
            current_app.logger.info(e)
            abort(500, description=ErrorMessages.SERVER_ERROR) 


