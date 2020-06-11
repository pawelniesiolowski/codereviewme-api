from app.code_review.controller.technology import setup_technology_controller
from app.code_review.controller.author import setup_author_controller
from app.code_review.controller.project import setup_project_controller
from app.code_review.controller.reviewer import setup_reviewer_controller


def setup_controllers(app):
    setup_technology_controller(app)
    setup_author_controller(app)
    setup_project_controller(app)
    setup_reviewer_controller(app)
