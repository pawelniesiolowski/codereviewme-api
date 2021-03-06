from app.code_review.model.project import Project
from tests.code_review.controller.fixture import (
    client,
    create_technology_and_return_id,
    auth_header_with_all_permissions
)


def test_it_creates_project_for_author(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client)
    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology_id],
    }
    resp = client.post(
        f'{author_href}/projects',
        json=project,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()

    assert '201' in resp.status
    assert len(projects) == 1
    assert resp_data['href'] == f'{author_href}/projects/{projects[0].id}'


def test_it_returns_404_if_author_does_not_exist(client):
    technology_id = create_technology_and_return_id(client)
    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology_id],
    }
    resp = client.post(
        f'authors/1/projects',
        json=project,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()

    assert '404' in resp.status
    assert len(projects) == 0
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_returns_422_if_project_does_not_have_technology(client):
    author_href = create_author_and_return_href(client)
    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
    }
    resp = client.post(
        f'{author_href}/projects',
        json=project,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()

    assert '422' in resp.status
    assert len(projects) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_returns_422_if_projects_technology_does_not_exist(client):
    author_href = create_author_and_return_href(client)
    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [1],
    }
    resp = client.post(
        f'{author_href}/projects',
        json=project,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()

    assert '422' in resp.status
    assert len(projects) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_edits_project(client):
    author_href = create_author_and_return_href(client)
    python_technology_id = create_technology_and_return_id(client, 'Python')
    js_technology_id = create_technology_and_return_id(client, 'JavaScript')
    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [python_technology_id],
    }
    project_href = client.post(
        f'{author_href}/projects',
        json=project_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']

    edited_project = {
        'name': 'Test Project v2',
        'technologies': [js_technology_id],
    }
    resp = client.patch(
        f'{project_href}',
        json=edited_project,
        headers=auth_header_with_all_permissions
    )
    projects = Project.query.filter(
        Project.name == edited_project['name']
    ).all()

    assert '204' in resp.status
    assert len(projects) == 1
    project = projects[0]
    assert len(project.technologies) == 1
    assert project.technologies[0].name == 'JavaScript'
    assert project.description == project_data['description']
    assert project.repository_url == project_data['repository_url']


def test_it_returns_404_if_edited_project_does_not_exist(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client)
    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology_id],
    }
    resp = client.patch(
        f'{author_href}/projects/1',
        json=project_data,
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()

    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_gets_project_by_id(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client, 'Python')
    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology_id],
    }
    project_href = client.post(
        f'{author_href}/projects',
        json=project_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']
    resp = client.get(project_href)
    resp_data = resp.get_json()['data']
    assert '200' in resp.status
    assert resp_data['name'] == 'Test Project'
    assert resp_data['technologies'][0]['name'] == 'Python'


def test_it_returns_404_if_project_does_not_exist(client):
    author_href = create_author_and_return_href(client)
    resp = client.get(f'{author_href}/projects/1')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_returns_all_projects_for_author(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client, 'Python')
    first_project_data = {
        'name': 'First Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawel/first_project',
        'technologies': [technology_id],
    }
    client.post(
        f'{author_href}/projects',
        json=first_project_data,
        headers=auth_header_with_all_permissions
    )
    second_project_data = {
        'name': 'Second Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawel/second_project',
        'technologies': [technology_id],
    }
    client.post(
        f'{author_href}/projects',
        json=second_project_data,
        headers=auth_header_with_all_permissions
    )
    resp = client.get(f'{author_href}/projects')
    resp_data = resp.get_json()['data']
    assert '200' in resp.status
    assert len(resp_data) == 2


def test_returns_404_if_author_does_not_have_any_projects(client):
    author_href = create_author_and_return_href(client)
    resp = client.get(f'{author_href}/projects')
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_deletes_project_for_author(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client, 'Python')
    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawel/first_project',
        'technologies': [technology_id],
    }
    project_href = client.post(
        f'{author_href}/projects',
        json=project_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']
    resp = client.delete(
        project_href,
        headers=auth_header_with_all_permissions
    )
    projects = Project.query.filter(Project.name == 'Test Project').all()
    assert '204' in resp.status
    assert len(projects) == 0


def test_it_returns_404_if_project_for_author_does_not_exist(client):
    resp = client.delete(
        'authors/1/projects/1',
        headers=auth_header_with_all_permissions
    )
    resp_data = resp.get_json()
    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def create_author_and_return_href(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    return client.post(
        '/authors',
        json=author_data,
        headers=auth_header_with_all_permissions
    ).get_json()['href']
