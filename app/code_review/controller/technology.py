from flask import request, jsonify, abort, url_for
from app import app
from app.code_review.model.technology import Technology
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from app.auth.auth import requires_auth


@app.route('/technologies', methods=['POST'])
@requires_auth('create:technology')
def create_technology():
    data = request.get_json()

    try:
        if Technology.query.filter(Technology.name == data['name']).all():
            abort(409)

        technology = Technology()
        if 'name' in data:
            technology.name = data.get('name', '')
        if 'description' in data:
            technology.description = data.get('description', '')
        if not technology.is_valid():
            abort(422)

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


@app.route('/technologies/<int:technology_id>', methods=['PATCH'])
@requires_auth('edit:technology')
def edit_technology(technology_id):
    data = request.get_json()

    try:
        technology = Technology.query.get(technology_id)

        if technology is None:
            abort(404)

        if 'name' in data:
            if (
                Technology.query
                    .filter(Technology.name == data['name'])
                    .all()
            ):
                abort(409)
            else:
                technology.name = data.get('name', '')

        if 'description' in data:
            technology.description = data.get('description', '')

        if not technology.is_valid():
            abort(422)

        technology.update()
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    return '', 204


@app.route('/technologies')
def index_technologies():
    try:
        technologies = Technology.query.all()
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    if not technologies:
        abort(404)

    formatted_technologies = [tech.format() for tech in technologies]
    return jsonify({'data': formatted_technologies})


@app.route('/technologies/<int:technology_id>', methods=['DELETE'])
@requires_auth('delete:technology')
def delete_technology(technology_id):
    try:
        technology = Technology.query.get(technology_id)

        if technology is None:
            abort(404)

        technology.delete()
    except SQLAlchemyError:
        abort(500)
    finally:
        db.session.close()

    return '', 204
