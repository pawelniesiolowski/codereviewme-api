import pytest
from app import create_app
from app.db import db, drop_everything
from config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    db.session.remove()
    drop_everything(db)
    db.create_all()
    client = app.test_client()
    yield client
