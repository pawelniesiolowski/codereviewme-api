from flask import request, jsonify, abort, url_for
from app import app
from app.code_review.model.author import Author
from app.code_review.model.project import Project
from app.code_review.model.technology import Technology
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from app.auth.auth import requires_auth


@app.route('/authors/<int:author_id>/projects', methods=['POST'])
@requires_auth('create:project')
def create_project(author_id):
    data = request.get_json()

    try:
        author = Author.query.get(author_id)
        if author is None:
            abort(404)
    except SQLAlchemyError:
        db.session.close()
        abort(500)

    project = Project(
        name=data.get('name', ''),
        description=data.get('description', ''),
        repository_url=data.get('repository_url', ''),
        author_id=author_id,
    )

    try:
        for technology_id in data.get('technologies', []):
            technology = Technology.query.get(technology_id)
            project.technologies.append(technology)

        if not project.is_valid():
            abort(422)

        project.insert()
        inserted_id = project.id
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    return jsonify(
        {
            'href': url_for(
                'get_project',
                author_id=author_id,
                project_id=inserted_id
            )
        }
    ), 201


@app.route('/authors/<int:author_id>/projects/<int:project_id>')
def get_project(author_id, project_id):
    try:
        project = Project.query.get(project_id)
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    if project is None or project.author_id != author_id:
        abort(404)

    return jsonify({'data': project.format()}), 200


@app.route('/authors/<int:author_id>/projects')
def index_projects(author_id):
    try:
        projects = Project.query.filter(
            Project.author_id == author_id
        ).all()
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    if len(projects) == 0:
        abort(404)

    formatted_projects = [project.format() for project in projects]
    return jsonify({'data': formatted_projects}), 200


@app.route(
    '/authors/<int:author_id>/projects/<int:project_id>',
    methods=['PATCH']
)
@requires_auth('edit:project')
def edit_project(author_id, project_id):
    data = request.get_json()

    try:
        author = Author.query.get(author_id)
        if author is None:
            abort(404)
        project = Project.query.get(project_id)
        if project is None:
            abort(404)
    except SQLAlchemyError:
        db.session.close()
        abort(500)

    if 'name' in data:
        project.name = data.get('name', '')
    if 'description' in data:
        project.description = data.get('description', '')
    if 'repository_url' in data:
        project.repository_url = data.get('repository_url', '')

    try:
        if 'technologies' in data:
            project.technologies = []
            for technology_id in data.get('technologies', []):
                technology = Technology.query.get(technology_id)
                project.technologies.append(technology)

        if not project.is_valid():
            abort(422)

        project.update()
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    return '', 204


@app.route(
    '/authors/<int:author_id>/projects/<int:project_id>',
    methods=['DELETE']
)
@requires_auth('delete:project')
def delete_project(author_id, project_id):
    try:
        project = Project.query.filter(
            Project.id == project_id,
            Project.author_id == author_id
        ).first()

        if project is None:
            abort(404)

        project.delete()
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    return '', 204
