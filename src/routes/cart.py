from flask import Blueprint, render_template, url_for, redirect, flash

from src.routes import product_test_values
from src.database.models.products import Product, InventoryEntries, InventoryEntryReasons
from src.authentication import user_details, login_required
from src.database.models.users import User

cart_route = Blueprint('cart', __name__)


@cart_route.get("/shopping-cart")
@user_details
async def get_cart(user: User | None):
    social_url = url_for('cart.get_cart', _external=True)
    customer = {
        "first_name": "joe"
    }
    products_list: list[Product] = product_test_values()
    context = dict(user=user, social_url=social_url, products_list=products_list, customer=customer)
    return render_template('cart/cart.html', **context)


@cart_route.get("/orders")
@user_details
async def get_orders(user: User | None):
    customer = {
        "first_name": "joe"
    }

    social_url = url_for('cart.get_orders', _external=True)
    context = dict(user=user, social_url=social_url, customer=customer)
    return render_template('orders/orders.html', **context)


@cart_route.post("/orders/<string:product_id>")
@login_required
async def place_orders(user: User, product_id: str):
    #TOD Capture Order Details Here
    # social_url = url_for('cart.get_orders', _external=True)
    # context = dict(user=user, social_url=social_url)
    flash(message="Order Successfully Captured", category="success")
    return redirect(url_for('cart.get_cart'))
