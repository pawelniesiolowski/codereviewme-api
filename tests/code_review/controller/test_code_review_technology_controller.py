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


def test_it_gets_technology(client):
    description = '''An interpreted, high-level,
general-purpose programming language'''
    data = {
        'name': 'Python',
        'description': description
    }
    post_resp = client.post('/technologies', json=data)
    post_resp_data = post_resp.get_json()
    get_resp = client.get(post_resp_data['href'])
    get_resp_data = get_resp.get_json()
    assert '200' in get_resp.status
    assert get_resp_data['data']['name'] == 'Python'
    assert get_resp_data['data']['description'] == description


def test_it_returns_404_if_technology_does_not_exist(client):
    resp = client.get('/technologies/1')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert 404 == resp_data['error']
    assert 'Not found' in resp_data['message']


def test_it_edits_technology(client):
    data = {
        'name': 'Python 3',
        'description': 'Programming language',
    }
    create_resp = client.post('/technologies', json=data)
    create_resp_data = create_resp.get_json()
    get_resp = client.get(create_resp_data['href'])
    get_resp_data = get_resp.get_json()
    edited_data = {
        'name': 'Python',
        'description': '''An interpreted, high-level,
general-purpose programming language''',
    }
    edit_resp = client.post(create_resp_data['href'], json=edited_data)
    assert '204' in edit_resp.status
    technologies = Technology.query.filter(Technology.name == 'Python').all()
    assert len(technologies) == 1


def test_it_returns_conflict_error_if_new_technology_name_exist(client):
    python_data = {
        'name': 'Python',
        'description': 'Object oriented programming language',
    }
    elixir_data = {
        'name': 'Elixir',
        'description': 'Functional programming language',
    }
    create_resp = client.post('/technologies', json=python_data)
    create_resp_data = create_resp.get_json()
    client.post('/technologies', json=elixir_data)
    edited_data = {
        'name': 'Elixir',
        'description': 'Object oriented programming language',
    }
    edited_resp = client.post(create_resp_data['href'], json=edited_data)
    edited_resp_data = edited_resp.get_json()
    assert '409' in edited_resp.status
    assert edited_resp_data['error'] == 409
    assert 'Entity already exists' in edited_resp_data['message']


def test_it_returns_404_if_edited_data_does_not_exist(client):
    data = {
        'name': 'Python',
        'description': 'Programming language',
    }
    resp = client.post('/technologies/1', json=data)
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert resp_data['message'] == 'Not found'


def test_index_technologies(client):
    python_data = {
        'name': 'Python',
        'description': 'Object oriented programming language',
    }
    elixir_data = {
        'name': 'Elixir',
        'description': 'Functional programming language',
    }
    client.post('/technologies', json=python_data)
    client.post('/technologies', json=elixir_data)
    resp = client.get('/technologies')
    resp_data = resp.get_json()
    assert '200' in resp.status
    assert len(resp_data['data']) == 2


def test_it_returns_404_when_there_is_no_technology(client):
    resp = client.get('/technologies')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_id_delete_technology(client):
    python_data = {
        'name': 'Python',
        'description': 'Object oriented programming language',
    }
    elixir_data = {
        'name': 'Elixir',
        'description': 'Functional programming language',
    }
    client.post('/technologies', json=python_data)
    create_resp = client.post('/technologies', json=elixir_data)
    create_resp_data = create_resp.get_json()
    resp = client.delete(create_resp_data['href'])
    assert '204' in resp.status
    assert len(Technology.query.all()) == 1


def test_it_returns_404_if_deleted_technology_does_not_exis(client):
    resp = client.delete('/technologies/1')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']
