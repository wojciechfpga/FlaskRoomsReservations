from app.models import db, User

class UserRepository:
    @staticmethod
    def get_user_by_username(username):
        return db.session.query(User).filter_by(username=username).first()

    @staticmethod
    def create_user(username, password, role):
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def user_exists(username):
        return db.session.query(User).filter_by(username=username).first() is not None
