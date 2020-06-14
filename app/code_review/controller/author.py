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

    @app.route('/authors')
    def index_authors():
        try:
            authors = Author.query.all()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        if len(authors) == 0:
            abort(404)

        formatted_authors = [author.format() for author in authors]

        return jsonify({'data': formatted_authors}), 200

    @app.route('/authors/<int:author_id>')
    def get_author(author_id):
        try:
            author = Author.query.get(author_id)
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        if author is None:
            abort(404)

        return jsonify({'data': author.format()}), 200

    @app.route('/authors/<int:author_id>', methods=['PATCH'])
    def edit_author(author_id):
        data = request.get_json()

        try:
            author = Author.query.get(author_id)

            if author is None:
                abort(404)

            if 'name' in data:
                author.name = data.get('name', '')
            if 'surname' in data:
                author.surname = data.get('surname', '')
            if 'email' in data:
                author.email = data.get('email', '')
            if 'description' in data:
                author.description = data.get('description', '')
            if 'technologies' in data:
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

    @app.route('/authors/<int:author_id>', methods=['DELETE'])
    def delete_author(author_id):
        try:
            author = Author.query.get(author_id)
            if author is None:
                abort(404)
            author.delete()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return '', 204
