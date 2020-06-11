from app.code_review.model.project import Project
from tests.code_review.controller.fixture import client


def test_it_creates_project_for_author(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client)
    project = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology_id],
    }
    resp = client.post(f'{author_href}/projects', json=project)
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
    resp = client.post(f'authors/1/projects', json=project)
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
    resp = client.post(f'{author_href}/projects', json=project)
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
    resp = client.post(f'{author_href}/projects', json=project)
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
        json=project_data
    ).get_json()['href']

    project_data['name'] = 'Test Project v2'
    project_data['technologies'] = [js_technology_id]
    resp = client.post(f'{project_href}', json=project_data)
    projects = Project.query.filter(Project.name == project_data['name']).all()

    assert '204' in resp.status
    assert len(projects) == 1
    assert len(projects[0].technologies) == 1
    assert projects[0].technologies[0].name == 'JavaScript'


def test_it_returns_404_if_edited_project_does_not_exist(client):
    author_href = create_author_and_return_href(client)
    technology_id = create_technology_and_return_id(client)
    project_data = {
        'name': 'Test Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawelniesiolowski/test_project',
        'technologies': [technology_id],
    }
    resp = client.post(f'{author_href}/projects/1', json=project_data)
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
        f'{author_href}/projects', json=project_data
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
    client.post(f'{author_href}/projects', json=first_project_data)
    second_project_data = {
        'name': 'Second Project',
        'description': 'Test description.',
        'repository_url': 'https://github.com/pawel/second_project',
        'technologies': [technology_id],
    }
    client.post(f'{author_href}/projects', json=second_project_data)
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


def create_author_and_return_href(client):
    author_data = {
        'name': 'Paweł',
        'surname': 'Niesiołowski',
        'email': 'test@gmail.com',
    }
    return client.post('/authors', json=author_data).get_json()['href']


def create_technology_and_return_id(client, name='Python'):
    technology_data = {
        'name': name,
        'description': 'Programming language.',
    }
    technology_href = client.post(
        '/technologies',
        json=technology_data
    ).get_json()['href']
    return client.get(technology_href).get_json()['data']['id']
