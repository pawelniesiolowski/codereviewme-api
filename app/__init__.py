from flask import Flask
from config import create_config_for_environment
from app.code_review.controller import setup_controllers
from app.db import db, init_db


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = create_config_for_environment()

    app.config.from_object(config)

    init_db(app, db)

    setup_controllers(app)

    return app
