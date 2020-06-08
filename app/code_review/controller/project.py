from flask import request, jsonify, abort, url_for
from app.code_review.model.author import Author
from app.code_review.model.project import Project
from app.code_review.model.technology import Technology
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


def setup_project_controller(app):

    @app.route('/authors/<int:author_id>/projects', methods=['POST'])
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
        pass