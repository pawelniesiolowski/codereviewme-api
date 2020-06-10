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


def test_it_edits_project(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    author_href = client.post('/authors', json=author_data).get_json()['href']
    author = client.get(author_href).get_json()['data']

    python_technology_data = {
        'name': 'Python',
        'description': 'Programming language.',
    }
    python_technology_href = client.post(
        '/technologies',
        json=python_technology_data
    ).get_json()['href']
    python_technology = client.get(python_technology_href).get_json()['data']

    js_technology_data = {
        'name': 'JavaScript',
        'description': 'Programming language.',
    }
    js_technology_href = client.post(
        '/technologies',
        json=js_technology_data
    ).get_json()['href']
    js_technology = client.get(js_technology_href).get_json()['data']

    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [python_technology['id']],
    }
    project_href = client.post(
        f'{author_href}/projects',
        json=project_data
    ).get_json()['href']

    project_data['name'] = 'Test Project v2'
    project_data['technologies'] = [js_technology['id']]

    resp = client.post(f'{project_href}', json=project_data)
    projects = Project.query.filter(Project.name == project_data['name']).all()

    assert '204' in resp.status
    assert len(projects) == 1
    assert len(projects[0].technologies) == 1
    assert projects[0].technologies[0].name == 'JavaScript'


def test_it_returns_404_if_edited_project_does_not_exist(client):
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

    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology['id']],
    }

    resp = client.post(f'{author_href}/projects/1', json=project_data)
    resp_data = resp.get_json()

    assert '404' in resp.status
    assert resp_data['error'] == 404
    assert 'Not found' in resp_data['message']
