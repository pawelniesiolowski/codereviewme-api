from flask import request, jsonify, abort, url_for
from app.code_review.model.author import Author
from app.code_review.model.technology import Technology
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


def setup_author_controller(app):

    @app.route('/authors', methods=['POST'])
    def create_author():
        data = request.get_json()
        author = Author(
            name=data.get('name', ''),
            surname=data.get('surname', ''),
            email=data.get('email', ''),
            description=data.get('description', ''),
        )

        try:
            for technology_id in data.get('technologies', []):
                technology = Technology.query.get(technology_id)
                author.technologies.append(technology)

            if not author.is_valid():
                abort(422)

            author.insert()
            inserted_id = author.id
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return jsonify(
            {'href': url_for('get_author', author_id=inserted_id)}
        ), 201

    @app.route('/authors/<int:author_id>')
    def get_author(author_id):
        pass

    @app.route('/authors/<int:author_id>', methods=['POST'])
    def edit_author(author_id):
        data = request.get_json()

        try:
            author = Author.query.get(author_id)

            if author is None:
                abort(404)

            author.name = data.get('name', '')
            author.surname = data.get('surname', '')
            author.email = data.get('email', '')
            author.description = data.get('description', '')
            author.technologies = []

            for technology_id in data.get('technologies', []):
                technology = Technology.query.get(technology_id)
                author.technologies.append(technology)

            if not author.is_valid():
                abort(422)

            author.update()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return '', 204
