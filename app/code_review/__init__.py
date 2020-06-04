from app.code_review.controller import setup_controllers


def setup_module(app):
    setup_controllers(app)
