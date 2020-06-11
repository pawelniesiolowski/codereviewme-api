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


def create_technology_and_return_id(client, name='Python'):
    technology_data = {
        'name': name,
        'description': 'Programming language.',
    }
    technology_href = client.post(
        '/technologies',
        json=technology_data
    ).get_json()['href']
    return client.get(technology_href).get_json()['data']['id']
