import pytest
from app import app
from app.db import db, drop_everything
from config import TestingConfig
from app.auth.auth_token import create_auth_header_with_permissions


@pytest.fixture
def client():
    app.config.from_object(TestingConfig())
    db.session.remove()
    drop_everything(db)
    db.create_all()
    client = app.test_client()
    yield client


auth_header_with_all_permissions = create_auth_header_with_permissions(
    domain=TestingConfig.AUTH0_DOMAIN,
    api_audience=TestingConfig.API_AUDIENCE,
    client_id=TestingConfig.CLIENT_ID,
    client_secret=TestingConfig.CLIENT_SECRET
)


def create_technology_and_return_id(client, name='Python'):
    technology_data = {
        'name': name,
        'description': 'Programming language.',
    }
    technology_href = client.post(
        '/technologies',
        json=technology_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']
    return client.get(technology_href).get_json()['data']['id']
