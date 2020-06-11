from flask import request, jsonify, abort, url_for
from app.code_review.model.reviewer import Reviewer
from app.code_review.model.technology import Technology
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


def setup_reviewer_controller(app):

    @app.route('/reviewers', methods=['POST'])
    def create_reviewer():
        data = request.get_json()
        reviewer = Reviewer(
            name=data.get('name', ''),
            surname=data.get('surname', ''),
            email=data.get('email', ''),
            description=data.get('description', ''),
            repository_url=data.get('repository_url', '')
        )

        try:
            for technology_id in data.get('technologies', []):
                technology = Technology.query.get(technology_id)
                reviewer.technologies.append(technology)

            if not reviewer.is_valid():
                abort(422)

            reviewer.insert()
            inserted_id = reviewer.id
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return jsonify(
            {'href': url_for('get_reviewer', reviewer_id=inserted_id)}
        ), 201

    @app.route('/reviewers')
    def index_reviewers():
        try:
            reviewers = Reviewer.query.all()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        if len(reviewers) == 0:
            abort(404)

        formatted_reviewers = [reviewer.format() for reviewer in reviewers]

        return jsonify({'data': formatted_reviewers}), 200

    @app.route('/reviewers/<int:reviewer_id>')
    def get_reviewer(reviewer_id):
        try:
            reviewer = Reviewer.query.get(reviewer_id)
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        if reviewer is None:
            abort(404)

        return jsonify({'data': reviewer.format()}), 200

    @app.route('/reviewers/<int:reviewer_id>', methods=['POST'])
    def edit_reviewer(reviewer_id):
        data = request.get_json()

        try:
            reviewer = Reviewer.query.get(reviewer_id)

            if reviewer is None:
                abort(404)

            reviewer.name = data.get('name', '')
            reviewer.surname = data.get('surname', '')
            reviewer.email = data.get('email', '')
            reviewer.description = data.get('description', '')
            reviewer.repository_url = data.get('repository_url', '')
            reviewer.technologies = []

            for technology_id in data.get('technologies', []):
                technology = Technology.query.get(technology_id)
                reviewer.technologies.append(technology)

            if not reviewer.is_valid():
                abort(422)

            reviewer.update()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return '', 204

    @app.route('/reviewers/<int:reviewer_id>', methods=['DELETE'])
    def delete_reviewer(reviewer_id):
        try:
            reviewer = Reviewer.query.get(reviewer_id)
            if reviewer is None:
                abort(404)
            reviewer.delete()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return '', 204
