from flask import Flask
from config import create_config_for_environment
from app.student import controller as student_controller
from app.reviewer import controller as reviewer_controller


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = create_config_for_environment()

    app.config.from_object(config)

    student_controller.setup_controllers(app)
    reviewer_controller.setup_controllers(app)

    return app
