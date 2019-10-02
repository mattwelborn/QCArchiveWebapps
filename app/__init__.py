from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    with app.app_context():

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        from .api import api as api_blueprint
        app.register_blueprint(api_blueprint, url_prefix='/api/v1')

        register_dashapps(flask_server=app)

        # Compile assets
        from .assets import compile_assets
        compile_assets(app)

        return app

    return app


def register_dashapps(flask_server):
    """Register dash apps using the flask server"""
     # Import Dash application

    from .dash_apps.dash_example import index as dash_example_index
    flask_server = dash_example_index.Add_Dash(flask_server, '/dash_example/')

    from .dash_apps.reaction_viewer import index as reaction_viewer_index
    flask_server = reaction_viewer_index.Add_Dash(flask_server, '/reaction_viewer/')

    return flask_server