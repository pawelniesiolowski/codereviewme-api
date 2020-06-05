from flask import jsonify


def setup_errors(app):

    @app.errorhandler(422)
    def validation_error(error):
        return jsonify({
            'error': 422,
            'message': 'Validation error'
        }), 422

    @app.errorhandler(500)
    def validation_error(error):
        return jsonify({
            'error': 500,
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(409)
    def validation_error(error):
        return jsonify({
            'error': 409,
            'message': 'Entity already exists'
        }), 409

    @app.errorhandler(404)
    def validation_error(error):
        return jsonify({
            'error': 404,
            'message': 'Not found'
        }), 404
