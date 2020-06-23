from flask import Flask
from flask_cors import CORS
from flask.logging import default_handler
from config import create_config_for_environment
from app.code_review import setup_module as setup_code_review
from app.db import db, init_db
from app.errors import setup_errors
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

    setup_errors(app)
    setup_code_review(app)

    return app


app = create_app()


@app.route('/')
def info():
    return 'Experience is the name everyone gives to their mistakes'
