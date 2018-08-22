from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from config import config
# from .api_1_0 import api_bp
# from .api_1_0.users import api_bp

db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
# api = Api()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    CSRFProtect(app)
    # api.init_app(api_bp)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api_1_0 import api as api_1_0_blueprint
    # from .api_1_0.users import api_bp as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
