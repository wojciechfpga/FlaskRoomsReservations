import pytest
from flask import Flask
from app import create_app
from unittest.mock import patch

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config["SECRET_KEY"] = "testsecretkey"
    return app

@pytest.fixture(scope='function')
def mock_db_session():
    with patch('app.models.db.session') as mock:
        yield mock

@pytest.fixture(scope='function')
def mock_reservation_model():
    with patch('app.models.Reservation') as mock:
        yield mock

@pytest.fixture(scope='function')
def mock_time_conflict():
    with patch('app.services.room_service.is_time_conflict') as mock:
        yield mock

