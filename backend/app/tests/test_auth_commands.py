import pytest
from app.commands.auth_commands import RegisterUserCommand
from app.constants.errors import ErrorMessages
from app.constants.tests_constants_auth_commands import TestsConstants

def test_register_user_missing_fields(app):
    with app.app_context():
        with pytest.raises(Exception) as excinfo:
            RegisterUserCommand.execute(TestsConstants.NO_USER_NAME,
                                        TestsConstants.TEST_PASSWORD,
                                        TestsConstants.TEST_ROLE)
        assert ErrorMessages.INVALID_AUTH in str(excinfo.value)
