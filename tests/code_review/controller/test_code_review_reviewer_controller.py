from app.code_review.model.reviewer import Reviewer
from tests.code_review.controller.fixture import (
    client,
    create_technology_and_return_id,
    auth_header_with_all_permissions
)


def test_it_creates_reviewer(client):
    technology_id = create_technology_and_return_id(client, 'Python')
    reviewer_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    resp = client.post(
        '/reviewers',
        json=reviewer_data,
        headers=auth_header_with_all_permissions
    )
    reviewer_href = resp.get_json()['href']
    reviewers = Reviewer.query.filter(Reviewer.surname == 'Niesiołowski').all()

    assert '201' in resp.status
    assert len(reviewers) == 1
    assert reviewer_href == f'/reviewers/{reviewers[0].id}'


def test_it_returns_422_if_reviewer_does_not_have_any_technology(client):
    technology_id = create_technology_and_return_id(client, 'Python')
    reviewer_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': '',
    }
    resp = client.post(
        '/reviewers',
        json=reviewer_data,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    reviewers = Reviewer.query.filter(Reviewer.surname == 'Niesiołowski').all()

    assert '422' in resp.status
    assert len(reviewers) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_edits_reviewer(client):
    python_id = create_technology_and_return_id(client, 'Python')
    elixir_id = create_technology_and_return_id(client, 'Elixir')
    new_reviewer_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'description': 'Experienced programmer.',
        'technologies': [python_id],
    }
    reviewer_href = client.post(
        '/reviewers',
        json=new_reviewer_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']

    edited_reviewer_data = {
        'description': 'Very experienced programmer.',
        'technologies': [python_id, elixir_id],
    }

    resp = client.patch(
        reviewer_href,
        json=edited_reviewer_data,
        headers=auth_header_with_all_permissions
    )
    reviewers = Reviewer.query.filter(
        Reviewer.description == 'Very experienced programmer.'
    ).all()

    assert '204' in resp.status
    assert len(reviewers) == 1
    assert len(reviewers[0].technologies) == 2


def test_it_returns_404_if_edited_reviewer_does_not_exists(client):
    resp = client.patch(
        '/reviewers/1',
        json=[],
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_gets_reviewer(client):
    technology_id = create_technology_and_return_id(client, 'Python')
    reviewer_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    reviewer_href = client.post(
        '/reviewers',
        json=reviewer_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']

    resp = client.get(reviewer_href)
    resp_data = resp.get_json()['data']

    assert '200' in resp.status
    assert resp_data['name'] == 'Paweł'
    assert resp_data['surname'] == 'Niesiołowski'
    assert resp_data['email'] == 'test@gmail.com'
    assert len(resp_data['technologies']) == 1
    assert resp_data['technologies'][0]['name'] == 'Python'


def test_it_returns_404_if_reviewer_does_not_exist(client):
    resp = client.get('/reviewers/1')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_indexes_reviewers(client):
    technology_id = create_technology_and_return_id(client, 'Python')
    first_reviewer = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    second_reviewer = {
        'name': 'Gal',
        'surname': 'Anonim',
        'email': 'anonim@gmail.com',
        'technologies': [technology_id],
    }
    client.post(
        '/reviewers',
        json=first_reviewer,
        headers=auth_header_with_all_permissions
    )
    client.post(
        '/reviewers',
        json=second_reviewer,
        headers=auth_header_with_all_permissions
    )
    resp = client.get('/reviewers')
    resp_data = resp.get_json()['data']
    assert '200' in resp.status
    assert len(resp_data) == 2


def test_it_returns_404_if_there_is_not_any_reviewer(client):
    resp = client.get('/reviewers')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_deletes_reviewer(client):
    technology_id = create_technology_and_return_id(client, 'Python')
    data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    created_reviewer_href = client.post(
        '/reviewers',
        json=data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']
    reviewers_before_delete = Reviewer.query.all()
    resp = client.delete(
        created_reviewer_href,
        headers=auth_header_with_all_permissions
    )
    reviewers_after_delete = Reviewer.query.all()
    assert '204' in resp.status
    assert len(reviewers_before_delete) == 1
    assert len(reviewers_after_delete) == 0


def test_it_returns_404_if_deleted_reviewer_does_not_exist(client):
    resp = client.delete(
        '/reviewers/1',
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']
