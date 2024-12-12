from app.models import db, Reservation
from datetime import datetime

def is_time_conflict(room_id, start_time, end_time):
    """
    Conflict checking
    """
    conflict = db.session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).first()
    return conflict is not None
