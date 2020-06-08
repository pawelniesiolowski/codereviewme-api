from app.code_review.model.project import Project
from tests.code_review.controller.fixture import client


def test_it_creates_project_for_author(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    author_href = client.post('/authors', json=author_data).get_json()['href']
    author = client.get(author_href).get_json()['data']

    technology_data = {
        'name': 'Python',
        'description': 'Programming language.',
    }
    technology_href = client.post(
        '/technologies',
        json=technology_data
    ).get_json()['href']
    technology = client.get(technology_href).get_json()['data']

    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology['id']],
    }
    resp = client.post(f'{author_href}/projects', json=project)
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()
    assert '201' in resp.status
    assert len(projects) == 1
    assert resp_data['href'] == f'{author_href}/projects/{projects[0].id}'


def test_it_returns_404_if_author_does_not_exist(client):
    technology_data = {
        'name': 'Python',
        'description': 'Programming language.',
    }
    technology_href = client.post(
        '/technologies',
        json=technology_data
    ).get_json()['href']
    technology = client.get(technology_href).get_json()['data']

    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology['id']],
    }
    resp = client.post(f'authors/1/projects', json=project)
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()
    assert '404' in resp.status
    assert len(projects) == 0
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']


def test_it_returns_422_if_project_does_not_have_technology(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    author_href = client.post('/authors', json=author_data).get_json()['href']
    author = client.get(author_href).get_json()['data']

    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
    }
    resp = client.post(f'{author_href}/projects', json=project)
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()
    assert '422' in resp.status
    assert len(projects) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']


def test_it_returns_422_if_projects_technology_does_not_exist(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    author_href = client.post('/authors', json=author_data).get_json()['href']
    author = client.get(author_href).get_json()['data']

    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [1],
    }
    resp = client.post(f'{author_href}/projects', json=project)
    resp_data = resp.get_json()
    projects = Project.query.filter(Project.name == 'Test Project').all()
    assert '422' in resp.status
    assert len(projects) == 0
    assert resp_data['error'] == 422
    assert 'Validation error' in resp_data['message']
