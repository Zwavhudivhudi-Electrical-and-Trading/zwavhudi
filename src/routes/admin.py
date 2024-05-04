from flask import Blueprint, render_template, url_for

from src.routes import product_test_values
from src.database.models.products import Product
from src.authentication import user_details, login_required
from src.database.models.users import User

admin_route = Blueprint('admin', __name__)


@admin_route.get('/admin/orders')
@login_required
async def get_orders(user: User):
    pass


@admin_route.get('/admin/customers')
@login_required
async def get_customers(user: User):
    pass


@admin_route.get('/admin/products')
@login_required
async def get_products(user: User):

    products_list: list[Product] = product_test_values()
    context = dict(user=user, products_list=products_list)
    return render_template('admin/products/products.html', **context)


@admin_route.get('/admin/messages')
@login_required
async def get_messages(user: User):
    pass
