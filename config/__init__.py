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
    API_AUDIENCE = 'https://codereviewme.org/api'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///codereviewme'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///codereviewme_test'


def create_config_for_environment():
    environment = environ.get('FLASK_ENV', Environment.PRODUCTION)
    if environment == Environment.PRODUCTION:
        return ProductionConfig
    if environment == Environment.DEVELOPMENT:
        return DevelopmentConfig
    if environment == Environment.TEST:
        return TestingConfig
