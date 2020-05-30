from config import TestingConfig
from app import create_app
import pytest


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    client = app.test_client()
    yield client
