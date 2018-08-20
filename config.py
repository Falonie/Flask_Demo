import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = "587"
    # MAIL_PORT = "465"
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    # MAIL_DEBUG : default app.debug
    MAIL_USERNAME = "541002901@qq.com"
    MAIL_PASSWORD = "ecerlujhbaahbdib"
    MAIL_DEFAULT_SENDER = "541002901@qq.com"
    ADMIN = "541002901@qq.com"
    FLASKY_POSTS_PER_PAGE = 7
    FLASKY_COMMENTS_PER_PAGE = 6
    FLASKY_ARTICLES_PER_PAGE = 6
    CELERY_RESULT_BACKEND = "redis://:falonie@127.0.0.1:6379/0"
    CELERY_BROKER_URL = "redis://:falonie@127.0.0.1:6379/0"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/flask_demo"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/flask_demo_test"
    WTF_CSRF_ENABLED = False


config = {
    'develop': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig
}