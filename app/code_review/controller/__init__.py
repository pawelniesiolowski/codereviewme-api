from app.code_review.controller.technology import setup_technology_controller


def setup_controllers(app):
    setup_technology_controller(app)
