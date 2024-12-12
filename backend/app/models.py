from app import db
from sqlalchemy import Index
from werkzeug.security import generate_password_hash, check_password_hash

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    room = db.relationship("Room", backref="reservations")
    user = db.relationship("User", backref="reservations_backref", overlaps="user")  # Unikalny backref i overlaps
    
    __table_args__ = (
        Index('idx_room_time', 'room_id', 'start_time', 'end_time', postgresql_where=(db.text("is_deleted = FALSE"))),
        Index('idx_room_id', 'room_id'),
        Index('idx_reservation_time', 'start_time', 'end_time'),
    )


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="employee")

    reservations = db.relationship("Reservation", backref="reservation_user", lazy='dynamic', overlaps="user")  # Unikalny backref i overlaps

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




