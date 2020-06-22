from os import environ


class Environment:
    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    TEST = 'test'


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH0_DOMAIN = 'intodevnull.eu.auth0.com'
    ALGORITHMS = ['RS256']
    API_AUDIENCE = environ.get('API_AUDIENCE')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///codereviewme'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///codereviewme_test'
    CLIENT_ID = environ.get('CLIENT_ID')
    CLIENT_SECRET = environ.get('CLIENT_SECRET')


def create_config_for_environment():
    environment = environ.get('FLASK_ENV', Environment.PRODUCTION)
    if environment == Environment.PRODUCTION:
        return ProductionConfig
    if environment == Environment.DEVELOPMENT:
        return DevelopmentConfig
    if environment == Environment.TEST:
        return TestingConfig
