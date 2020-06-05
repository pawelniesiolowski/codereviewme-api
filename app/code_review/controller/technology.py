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
        try:
            technology = Technology.query.get(technology_id)
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        if not technology:
            abort(404)

        return jsonify({'data': technology.format()}), 200

    @app.route('/technologies/<int:technology_id>', methods=['POST'])
    def edit_technology(technology_id):
        data = request.get_json()

        if not data['name'] and not data['description']:
            abort(422)

        try:
            technology = Technology.query.get(technology_id)

            if technology is None:
                abort(404)

            if data['name']:
                if (
                    Technology.query
                        .filter(Technology.name == data['name'])
                        .all()
                ):
                    abort(409)
                else:
                    technology.name = data['name']

            if data['description']:
                technology.description = data['description']

            technology.update()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        return '', 204

    @app.route('/technologies')
    def index():
        try:
            technologies = Technology.query.all()
        except SQLAlchemyError:
            abort(500)
        finally:
            db.session.close()

        if not technologies:
            abort(404)

        formated_technologies = [tech.format() for tech in technologies]
        return jsonify({'data': formated_technologies})
