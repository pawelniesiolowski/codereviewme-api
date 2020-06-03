def setup_controllers(app):

    @app.route('/reviewers')
    def reviewer_index():
        return 'reviewers index', 200
