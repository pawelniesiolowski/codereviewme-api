import pytest
from app import create_app
from app.db import db
from app.code_review.model import Reviewer
from config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    db.create_all()
    client = app.test_client()
    yield client
