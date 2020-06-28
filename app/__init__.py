from flask import Flask
from flask_cors import CORS
from flask.logging import default_handler
from config import create_config_for_environment
from app.db import db, init_db
from app.error_handlers import setup_error_handlers
from app.logger import setup_logger


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    if config is None:
        config = create_config_for_environment()

    app.config.from_object(config)

    app.logger.removeHandler(default_handler)
    setup_logger(app)

    init_db(app, db)

    setup_error_handlers(app)

    return app


app = create_app()


from app.code_review.controller import author, project, reviewer, technology  # noqa


@app.route('/')
def info():
    return 'Experience is the name everyone gives to their mistakes'
