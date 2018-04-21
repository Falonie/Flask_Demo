import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/flask_demo"
SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/flask_demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'develop': DevelopmentConfig,
    'default': DevelopmentConfig
}