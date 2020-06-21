from app.code_review.model.author import Author
from tests.code_review.controller.fixture import (
    client,
    create_technology_and_return_id,
    auth_header_with_all_permissions
)


def test_it_creates_author_without_technologies_and_projects(client):
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
    }
    resp = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    )
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
    resp = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    )
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
    resp = client.post(
        '/technologies',
        json=technology_data,
        headers=auth_header_with_all_permissions
    ).get_json()
    technology = client.get(resp['href']).get_json()['data']
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
        'technologies': [technology['id']],
    }
    resp = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    )
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
    resp = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '422' in resp.status
    assert len(authors) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_edits_given_authors_data(client):
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    author_href = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']
    edited_data = {
        'email': 'edit_test@gmail.com',
    }
    resp = client.patch(
        author_href,
        json=edited_data,
        headers=auth_header_with_all_permissions
    )
    authors = Author.query.filter(Author.email == 'edit_test@gmail.com').all()
    assert '204' in resp.status
    assert len(authors) == 1
    author = authors[0]
    assert author.name == 'Paweł'
    assert author.surname == 'Niesiołowski'


def test_it_changes_technologies_for_author(client):
    python_data = {
        'name': 'Python',
        'description': 'Programming language',
    }
    elixir_data = {
        'name': 'Elixir',
        'description': 'Programming language',
    }
    python_resp = client.post(
        '/technologies',
        json=python_data,
        headers=auth_header_with_all_permissions
    ).get_json()
    elixir_resp = client.post(
        '/technologies',
        json=elixir_data,
        headers=auth_header_with_all_permissions
    ).get_json()
    python_technology = client.get(python_resp['href']).get_json()['data']
    elixir_technology = client.get(elixir_resp['href']).get_json()['data']
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [python_technology['id']],
    }
    author_href = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']

    edited_data = {
        'technologies': [elixir_technology['id']],
    }
    resp = client.patch(
        author_href,
        json=edited_data,
        headers=auth_header_with_all_permissions
    )
    authors = Author.query.filter(Author.surname == 'Niesiołowski').all()
    assert '204' in resp.status
    assert len(authors) == 1
    assert len(authors[0].technologies) == 1
    assert authors[0].technologies[0].name == 'Elixir'


def test_it_returns_404_if_edited_author_does_not_exist(client):
    resp = client.patch(
        '/authors/1',
        json=[],
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_gets_author(client):
    technology_data = {
        'name': 'Python',
        'description': 'Programming language.',
    }
    create_technology_resp_data = client.post(
        '/technologies',
        json=technology_data,
        headers=auth_header_with_all_permissions
    ).get_json()
    technology = client.get(
        create_technology_resp_data['href']
    ).get_json()['data']
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Pasionate programmer.',
        'technologies': [technology['id']],
    }
    create_author_resp_data = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    ).get_json()
    resp = client.get(create_author_resp_data['href'])
    author = resp.get_json()['data']
    assert '200' in resp.status
    assert author['name'] == 'Paweł'
    assert author['surname'] == 'Niesiołowski'
    assert author['email'] == 'test@gmail.com'
    assert author['description'] == 'Pasionate programmer.'
    assert len(author['technologies']) == 1
    assert author['technologies'][0]['name'] == 'Python'
    assert author['technologies'][0]['description'] == 'Programming language.'


def test_it_returns_404_if_author_does_not_exist(client):
    resp = client.get('/authors/1')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_indexes_authors(client):
    first_author = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    second_author = {
        'name': 'Gal',
        'surname': 'Anonim',
        'email': 'anonim@gmail.com',
    }
    client.post(
        '/authors',
        json=first_author,
        headers=auth_header_with_all_permissions
    )
    client.post(
        '/authors',
        json=second_author,
        headers=auth_header_with_all_permissions
    )
    resp = client.get('/authors')
    resp_data = resp.get_json()['data']
    assert '200' in resp.status
    assert len(resp_data) == 2


def test_it_returns_404_if_there_is_not_any_author(client):
    resp = client.get('/authors')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_deletes_author(client):
    technology_id = create_technology_and_return_id(client, 'Python')
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    created_author_data = client.post(
        '/authors',
        json=data,
        headers=auth_header_with_all_permissions
    ).get_json()
    authors_before_delete = Author.query.all()
    resp = client.delete(
        created_author_data['href'],
        headers=auth_header_with_all_permissions
    )
    authors_after_delete = Author.query.all()
    assert '204' in resp.status
    assert len(authors_before_delete) == 1
    assert len(authors_after_delete) == 0


def test_it_returns_404_if_deleted_author_does_not_exist(client):
    resp = client.delete(
        '/authors/1',
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']
