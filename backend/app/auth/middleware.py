from functools import wraps
import jwt
from flask import request, jsonify, current_app
from app import db
from app.models import User
from app.constants.errors import ErrorMessages
from app.constants.middleware_strings import MiddlewareStrings

def authorization_jwt(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": ErrorMessages.INVALID_AUTH}), 401

            if token.startswith(MiddlewareStrings.TOKEN_START_WORD):
                token = token[7:]

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                user_id = data.get("user_id")
                user = db.session.query(User).filter_by(id=user_id).first()
                if not user or user.role not in allowed_roles:
                    return jsonify({"error": ErrorMessages.INVALID_AUTH}), 403
                kwargs['user_id'] = user_id
            except jwt.ExpiredSignatureError:
                return jsonify({"error": ErrorMessages.F_STRING_ERROR}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": ErrorMessages.INVALID_AUTH}), 401

            return f(*args, **kwargs)
        return decorated
    return decorator
