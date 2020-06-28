import logging


logger = logging.getLogger(__name__)


def setup_logger(app):
    formatter = logging.Formatter(
        '[%(asctime)s] - %(pathname)s:%(lineno)d - %(levelname)s: %(message)s',
        '%d-%m %H:%M:%S'
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(app.config['LOG_LEVEL'])
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setLevel(app.config['LOG_LEVEL'])
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
