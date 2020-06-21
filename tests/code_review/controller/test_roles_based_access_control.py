from tests.code_review.controller.fixture import (
    client,
    create_technology_and_return_id,
    auth_header_with_reviewer_permissions,
    auth_header_with_author_permissions,
    auth_header_with_codereviewme_admin_permissions
)


def test_reviewer_should_have_access_to_create_reviewer(client):
    technology_id = create_technology_and_return_id(client)
    reviewer_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    resp = client.post(
        '/reviewers',
        json=reviewer_data,
        headers=auth_header_with_reviewer_permissions
    )

    assert '201' in resp.status


def test_reviewer_should_not_have_access_to_create_author(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com'
    }
    resp = client.post(
        '/authors',
        json=author_data,
        headers=auth_header_with_reviewer_permissions
    )
    resp_data = resp.get_json()

    assert '401' in resp.status
    assert resp_data['error'] == 401


def test_author_should_have_access_to_create_author(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com'
    }
    resp = client.post(
        '/authors',
        json=author_data,
        headers=auth_header_with_author_permissions
    )

    assert '201' in resp.status


def test_author_should_not_have_access_to_create_reviewer(client):
    technology_id = create_technology_and_return_id(client)
    reviewer_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
        'technologies': [technology_id],
    }
    resp = client.post(
        '/reviewers',
        json=reviewer_data,
        headers=auth_header_with_author_permissions
    )
    resp_data = resp.get_json()

    assert '401' in resp.status
    assert resp_data['error'] == 401


def test_codereviewme_admin_should_have_access_to_create_technology(client):
    technology_data = {
        'name': 'Python'
    }
    resp = client.post(
        '/technologies',
        json=technology_data,
        headers=auth_header_with_codereviewme_admin_permissions
    )

    assert '201' in resp.status


def test_codereviewme_admin_should_not_have_access_to_create_author(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com'
    }
    resp = client.post(
        '/authors',
        json=author_data,
        headers=auth_header_with_codereviewme_admin_permissions
    )
    resp_data = resp.get_json()

    assert '401' in resp.status
    assert resp_data['error'] == 401
