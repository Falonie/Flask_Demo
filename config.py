import os


class DevelopmentConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/flask_demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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


config = {
    'develop': DevelopmentConfig,
    'default': DevelopmentConfig
}