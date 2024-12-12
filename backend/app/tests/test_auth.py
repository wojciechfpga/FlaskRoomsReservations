import pytest
from app.commands.auth_commands import RegisterUserCommand

def test_register_user_missing_fields(app):
    with app.app_context():
        with pytest.raises(Exception) as excinfo:
            RegisterUserCommand.execute("", "testpassword", "user")
        assert "Username and password are required" in str(excinfo.value)
