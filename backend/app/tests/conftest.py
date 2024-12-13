import pytest
from flask import Flask
from app import create_app
from unittest.mock import patch

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config["SECRET_KEY"] = "testsecretkey"
    return app