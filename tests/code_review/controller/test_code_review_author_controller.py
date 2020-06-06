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
