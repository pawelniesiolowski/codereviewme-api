from flask import Flask
from flask_cors import CORS
from config import create_config_for_environment
from app.code_review import setup_module as setup_code_review
from app.db import db, init_db
from app.errors import setup_errors


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    if config is None:
        config = create_config_for_environment()

    app.config.from_object(config)

    init_db(app, db)

    setup_errors(app)
    setup_code_review(app)

    return app

app = create_app()
