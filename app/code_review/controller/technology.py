from flask import request, jsonify, abort, url_for
from app.code_review.model.technology import Technology
from app.db import db
from sqlalchemy.exc import SQLAlchemyError


def setup_technology_controller(app):

    @app.route('/technologies', methods=['POST'])
    def create_technology():
        data = request.get_json()

        if not data['name'] or not data['description']:
            abort(422)

        try:
            if Technology.query.filter(Technology.name == data['name']).all():
                abort(409)
            technology = Technology(
                name=data['name'],
                description=data['description'],
            )
            technology.insert()
            inserted_id = technology.id
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return jsonify(
            {'href': url_for('get_technology', technology_id=inserted_id)}
        ), 201

    @app.route('/technologies/<int:technology_id>')
    def get_technology(technology_id):
        pass
