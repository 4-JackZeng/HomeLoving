from flask import Flask

from user.house_views import house_blueprint
from user.order_views import order_blueprint

from user.user_views import user_blueprint, login_manager
from utils.Config import Config
from utils.funtions import init_ext
from utils.settings import TEMPLATES_DIR, STATIC_DIR


def create_user():

    app = Flask(__name__,static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)


    app.config.from_object(Config)


    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')

    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/homeloving'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SECRET_KEY'] = 'secret_key'

    login_manager.login_view = 'user.login'

    init_ext(app)

    return app

    # db.init_app(app)