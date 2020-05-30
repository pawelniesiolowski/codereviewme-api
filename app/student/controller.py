def setup_controllers(app):

    @app.route('/students')
    def student_index():
        return 'student index', 200
