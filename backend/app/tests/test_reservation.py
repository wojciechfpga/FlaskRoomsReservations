import pytest
from datetime import datetime, timedelta
from app.commands.reservation_commands import CreateReservationCommand, SoftDeleteReservationCommand


def test_create_reservation_invalid_time_range(app):
    with app.app_context():
        with pytest.raises(ValueError) as excinfo:
            CreateReservationCommand.execute(
                room_id=1,
                user_id=2,
                start_time=datetime.now() + timedelta(hours=1),
                end_time=datetime.now()
            )
        assert "Invalid time range" in str(excinfo.value)



def test_soft_delete_reservation_not_found(app, mock_db_session):
    with app.app_context():
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        with pytest.raises(ValueError) as excinfo:
            SoftDeleteReservationCommand.execute(reservation_id=1)
        assert "Reservation not found or already deleted" in str(excinfo.value)

def test_soft_delete_reservation_already_deleted(app, mock_db_session, mocker):
    with app.app_context():
        mock_reservation = mocker.Mock(is_deleted=True)
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_reservation

        with pytest.raises(ValueError) as excinfo:
            SoftDeleteReservationCommand.execute(reservation_id=1)
        assert "Reservation not found or already deleted" in str(excinfo.value)
