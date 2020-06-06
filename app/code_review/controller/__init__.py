from app.code_review.controller.technology import setup_technology_controller
from app.code_review.controller.author import setup_author_controller


def setup_controllers(app):
    setup_technology_controller(app)
    setup_author_controller(app)
