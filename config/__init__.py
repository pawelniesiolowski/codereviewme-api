from os import environ

class Environment:
    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    TEST = 'test'

class Config:
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

def create_config_for_environment():
    environment = environ.get('FLASK_ENV', Environment.PRODUCTION)
    if environment == Environment.PRODUCTION:
        return ProductionConfig
    if environment == Environment.DEVELOPMENT:
        return DevelopmentConfig
    if environment == Environment.TEST:
        return TestingConfig
