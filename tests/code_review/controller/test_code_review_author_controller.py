from app.code_review.model.author import Author
from app.code_review.model.project import Project
from tests.code_review.controller.fixture import client


def test_it_creates_author_without_technologies_and_projects(client):
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
    }
    resp = client.post('/authors', json=data)
    resp_data = resp.get_json()
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '201' in resp.status
    assert len(authors) == 1
    assert resp_data['href'] == f'/authors/{authors[0].id}'


def test_it_returns_404_if_author_data_is_invalid(client):
    data = {
        'name': 'Paweł',
        'surname': '',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
    }
    resp = client.post('/authors', json=data)
    resp_data = resp.get_json()
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '422' in resp.status
    assert len(authors) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_creates_author_with_technology(client):
    technology_data = {
        'name': 'Python',
        'description': 'Programming language',
    }
    resp = client.post('/technologies', json=technology_data).get_json()
    technology = client.get(resp['href']).get_json()['data']
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
        'technologies': [technology['id']],
    }
    resp = client.post('/authors', json=data)
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '201' in resp.status
    assert len(authors) == 1
    assert authors[0].technologies[0].name == 'Python'


def test_it_returns_validation_error_if_technology_does_not_exist(client):
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
        'technologies': [1],
    }
    resp = client.post('/authors', json=data)
    resp_data = resp.get_json()
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '422' in resp.status
    assert len(authors) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_edits_base_author_data(client):
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
    }
    create_resp_data = client.post('/authors', json=data).get_json()
    data['email'] = 'edit_test@gmail.com'
    resp = client.post(create_resp_data['href'], json=data)
    authors = Author.query.filter(Author.email == 'edit_test@gmail.com').all()
    assert '204' in resp.status
    assert len(authors) == 1


def test_it_changes_technologies_for_author(client):
    python_data = {
        'name': 'Python',
        'description': 'Programming language',
    }
    elixir_data = {
        'name': 'Elixir',
        'description': 'Programming language',
    }
    python_resp = client.post('/technologies', json=python_data).get_json()
    elixir_resp = client.post('/technologies', json=elixir_data).get_json()
    python_technology = client.get(python_resp['href']).get_json()['data']
    elixir_technology = client.get(elixir_resp['href']).get_json()['data']
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
        'technologies': [python_technology['id']],
    }
    create_resp_data = client.post('/authors', json=data).get_json()
    data['technologies'] = [elixir_technology['id']]
    resp = client.post(create_resp_data['href'], json=data)
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '204' in resp.status
    assert len(authors) == 1
    assert len(authors[0].technologies) == 1
    assert authors[0].technologies[0].name == 'Elixir'


def test_it_returns_404_if_edited_author_does_not_exist(client):
    resp = client.post('/authors/1', json=[])
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']
