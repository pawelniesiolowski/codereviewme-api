import pytest
from app import create_app
from app.db import db, drop_everything
from app.code_review.model.technology import Technology
from config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    db.session.remove()
    drop_everything(db)
    db.create_all()
    client = app.test_client()
    yield client


def test_it_creates_technology(client):
    data = {
        'name': 'Python',
        'description': '''An interpreted, high-level,
general-purpose programming language''',
    }
    resp = client.post('/technologies', json=data)
    resp_data = resp.get_json()
    assert '201' in resp.status

    technologies = Technology.query.filter(Technology.name == 'Python').all()
    assert len(technologies) == 1
    assert resp_data['href'] == f'/technologies/{technologies[0].id}'


def test_it_returns_validation_error_when_technology_data_is_invalid(client):
    data = {
        'name': '',
        'description': 'Description for empty name'
    }
    resp = client.post('/technologies', json=data)
    resp_data = resp.get_json()
    assert '422' in resp.status
    assert 422 == resp_data['error']
    assert 'Validation error' in resp_data['message']


def test_it_returns_conflict_error_when_technology_name_already_exists(client):
    data = {
        'name': 'Python',
        'description': '''An interpreted, high-level,
general-purpose programming language''',
    }
    data_with_already_added_name = {
        'name': 'Python',
        'description': 'Programming language',
    }
    client.post('/technologies', json=data)
    resp = client.post('/technologies', json=data_with_already_added_name)
    resp_data = resp.get_json()
    assert '409' in resp.status
    assert 409 == resp_data['error']
    assert 'Entity already exists' in resp_data['message']
