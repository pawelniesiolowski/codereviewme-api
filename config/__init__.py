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
    REVIEWER_CLIENT_ID = '6BhqOLSJBG7ftU1xLj5ZZYJ0Imv5RxhZ'
    REVIEWER_CLIENT_SECRET = (
        'gwr-S-ctQ3cIGqFA8d_RIA1MZf7MSpTiWpw0Y_vLEq7DdSYmzq1OAMkeTYTNxjvs'
    )
    AUTHOR_CLIENT_ID = 'xtpPzPzlz4j4JaZYiGmhgA7EGHizuyEb'
    AUTHOR_CLIENT_SECRET = (
        'getq6HcmCjrrmOvSkSNzoW2SE4DWVsc92HUDs5lfGtjs6YTQNZHg_TDzOiH-W4aL'
    )
    CODEREVIEWME_ADMIN_CLIENT_ID = 'TGuobWS2p4e0DIcD1TM92oXVUUd6hFvB'
    CODEREVIEWME_ADMIN_CLIENT_SECRET = (
        'Fn2XVsJa71xWVZ1mQWLSDfoYQokqstgusTWFmxBtPdSm7oETBWfBTUFCCjxWIfMN'
    )


def create_config_for_environment():
    environment = environ.get('FLASK_ENV', Environment.PRODUCTION)
    if environment == Environment.PRODUCTION:
        return ProductionConfig
    if environment == Environment.DEVELOPMENT:
        return DevelopmentConfig
    if environment == Environment.TEST:
        return TestingConfig
