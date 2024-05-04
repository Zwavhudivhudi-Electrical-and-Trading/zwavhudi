from flask import Blueprint, render_template, url_for

from src.authentication import user_details
from src.database.models.users import User

cart_route = Blueprint('cart', __name__)


@cart_route.get("/shopping-cart")
@user_details
async def get_cart(user: User | None):
    social_url = url_for('cart.get_cart', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('cart/cart.html', **context)


@cart_route.get("/orders")
@user_details
async def get_orders(user: User | None):
    social_url = url_for('cart.get_orders', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('orders/orders.html', **context)
