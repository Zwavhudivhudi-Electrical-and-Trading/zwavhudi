from flask import Blueprint, render_template, url_for, request, redirect, flash
from pydantic import ValidationError

from src.routes import product_test_values
from src.database.models.products import Product, Category
from src.authentication import user_details, login_required, admin_login
from src.database.models.users import User
from src.main import product_controller

admin_route = Blueprint('admin', __name__)


@admin_route.get('/admin/orders')
@admin_login
async def get_orders(user: User):
    pass


@admin_route.get('/admin/customers')
@admin_login
async def get_customers(user: User):
    pass


@admin_route.get('/admin/products')
@admin_login
async def get_products(user: User):
    products_list = await product_controller.get_products()
    category_list = await product_controller.get_categories()

    if not products_list:
        products_list: list[Product] = product_test_values()

    context = dict(user=user, category_list=category_list, products_list=products_list)
    return render_template('admin/products/products.html', **context)


@admin_route.get('/admin/categories')
@admin_login
async def get_categories(user: User):
    """

    :param user:
    :return:
    """
    products_list = await product_controller.get_products()
    category_list = await product_controller.get_categories()

    context = dict(user=user, category_list=category_list, products_list=products_list)
    return render_template('admin/products/categories.html', **context)


@admin_route.post('/admin/categories')
@admin_login
async def add_product_category(user: User):
    """

    :param user:
    :return:
    """
    try:
        category_detail = Category(**request.form)
        image = request.files['image']
        print(category_detail)

    except ValidationError as e:
        flash(message="Please include all category details", category="danger")
        return redirect(url_for('admin.get_categories'))
    image_link = await product_controller.save_category_image(category_name=category_detail.name, image=image)
    category_detail.img_link = image_link
    category_ = await product_controller.add_category(category_detail=category_detail)

    flash(message="Category added successfully", category="success")
    return redirect(url_for('admin.get_categories'))


@admin_route.get('/admin/messages')
@admin_login
async def get_messages(user: User):
    pass
