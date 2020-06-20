import pytest
import http.client
import json
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


def create_auth_header_with_all_scopes():
    conn = http.client.HTTPSConnection(TestingConfig.AUTH0_DOMAIN)
    payload = f'{{"client_id":"{TestingConfig.CLIENT_ID}",\
"client_secret":"{TestingConfig.CLIENT_SECRET}",\
"audience":"{TestingConfig.API_AUDIENCE}","grant_type":"client_credentials"}}'
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token = json.loads(data.decode('utf-8'))['access_token']
    return {'authorization': f'Bearer {token}'}


auth_header_with_all_scopes = create_auth_header_with_all_scopes()


def create_technology_and_return_id(client, name='Python'):
    technology_data = {
        'name': name,
        'description': 'Programming language.',
    }
    technology_href = client.post(
        '/technologies',
        json=technology_data,
        headers=auth_header_with_all_scopes
    ).get_json()['href']
    return client.get(technology_href).get_json()['data']['id']
