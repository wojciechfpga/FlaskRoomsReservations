from datetime import datetime, timedelta
import pytest
from werkzeug.exceptions import HTTPException

from app.commands.reservation_commands import CreateReservationCommand
from app.constants.errors import ErrorMessages
from app.constants.tests_constants_reservation_commands import TestsConstants


def test_create_reservation_invalid_time_range(app):
    with app.app_context():
        with pytest.raises(HTTPException) as excinfo:
            CreateReservationCommand.execute(
                room_id=TestsConstants.ID_OF_ROOM_TO_RAISE_TIME_CONFLICT,
                user_id=TestsConstants.ID_OF_USER_TO_RAISE_TIME_CONFLICT,
                start_time=datetime.now() + timedelta(hours=TestsConstants.HOURS_OF_OFFSET_TO_RAISE_TIME_CONFLICT),
                end_time=datetime.now()
            )
        assert excinfo.value.code == 409
        assert ErrorMessages.TIME_NOT_CORRECT in excinfo.value.description
