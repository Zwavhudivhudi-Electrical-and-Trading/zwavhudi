from flask import Flask
from flask_socketio import SocketIO
from src.controller.encryptor import Encryptor

from src.emailer import SendMail

from src.utils import format_with_grouping, friendlytimestamp

encryptor = Encryptor()
send_mail = SendMail()

from src.controller.auth import UserController
from src.controller.customers_controller import CustomerController
from src.controller.orders_controller import  OrdersController
from src.controller.paypal_controller import PayPalController
from src.controller.chat_controller import ChatController
from src.controller.messaging_controller import MessagingController

# from src.firewall import Firewall

user_controller = UserController()
customer_controller = CustomerController()
orders_controller = OrdersController()
paypal_controller = PayPalController()
chat_controller = ChatController()
messaging_controller = MessagingController()

chat_io = SocketIO()


# firewall = Firewall()
def _add_blue_prints(app: Flask):
    """
        this function adds blueprints
    :param app:
    :return:
    """
    from src.routes.home import home_route
    from src.routes.auth import auth_route
    from src.routes.cart import cart_route

    routes = [auth_route, home_route, cart_route]
    for route in routes:
        app.register_blueprint(route)


def _add_filters(app: Flask):
    """
        **add_filters**
            filters allows formatting from models to user readable format
    :param app:
    :return:
    """
    app.jinja_env.filters['number'] = format_with_grouping
    app.jinja_env.filters['time'] = friendlytimestamp


def create_app(config):
    from src.utils import template_folder, static_folder
    app: Flask = Flask(__name__)
    app.template_folder = template_folder()
    app.static_folder = static_folder()
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['BASE_URL'] = "https://dreamland-chemicals.org"

    with app.app_context():
        from src.main.bootstrapping import bootstrapper
        bootstrapper()
        # firewall.init_app(app=app)

        _add_blue_prints(app)
        _add_filters(app)
        encryptor.init_app(app=app)
        chat_io.init_app(app)
        user_controller.init_app(app=app)
        customer_controller.init_app(app=app)
        orders_controller.init_app(app=app)
        paypal_controller.init_app(app=app, config_instance=config)
        # chat_controller.init_app(app=app)
        # messaging_controller.init_app(app=app)

    return app
