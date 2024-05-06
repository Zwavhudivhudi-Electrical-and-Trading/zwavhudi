from flask import Blueprint, render_template, url_for, redirect, flash, request

from src.database.models.orders import Order, OrderItem
from src.database.models.customers import CustomerDetails
from src.main import customer_controller, product_controller

from src.database.models.products import Product, InventoryEntries, InventoryEntryReasons, Category
from src.authentication import user_details, login_required
from src.database.models.users import User

cart_route = Blueprint('cart', __name__)


@cart_route.get("/shopping-cart")
@user_details
async def get_cart(user: User | None):
    social_url = url_for('cart.get_cart', _external=True)

    customer_details = await customer_controller.get_customer_details(customer_id=user.customer_id)

    products_list: list[Product] = await product_controller.get_products()
    categories_list: list[Category] = await product_controller.get_categories()

    context = dict(user=user, social_url=social_url, category_list=categories_list, products_list=products_list,
                   customer=customer_details)
    return render_template('cart/cart.html', **context)


@cart_route.get("/shopping-cart/category/<string:category_name>")
@user_details
async def get_category_products(user: User | None, category_name: str):
    """

    :param user:
    :param category_name:
    :return:
    """
    category_details = await product_controller.get_category_details(category_name=category_name)
    products_list = await product_controller.get_category_products(category_id=category_details.category_id)
    context = dict(user=user, category=category_details, products_list=products_list)
    return render_template('cart/includes/category_products.html', **context)


@cart_route.get("/orders")
@user_details
async def get_orders(user: User | None):
    social_url = url_for('cart.get_orders', _external=True)

    customer_details = await customer_controller.get_customer_details(customer_id=user.customer_id)

    temp_orders: list[Order] = await customer_controller.get_temp_orders(customer_id=user.customer_id)

    context = dict(user=user, social_url=social_url, customer=customer_details, orders=temp_orders)
    return render_template('orders/orders.html', **context)


@cart_route.post("/orders/<string:product_id>")
@login_required
async def place_orders(user: User, product_id: str):
    order_quantity = request.form.get('quantity')

    if user.customer_id:
        customer_details: CustomerDetails | None = await customer_controller.get_customer_details(
            customer_id=user.customer_id)
        product_detail: Product | None = await product_controller.get_product(product_id=product_id)

        if customer_details:
            customer_name = f"{customer_details.full_names} {customer_details.surname}"
            email = customer_details.email if customer_details.email else user.email

            temp_order = await customer_controller.get_temp_orders(customer_id=user.customer_id)

            if not temp_order:
                temp_order = Order(customer_id=user.customer_id, customer_name=customer_name, email=email,
                                   phone=customer_details.contact_number,
                                   address_id=customer_details.delivery_address_id,
                                   items_ordered=[])

                saved_temp_order = await customer_controller.add_temp_order(order=temp_order)

            order_item = OrderItem(order_id=temp_order.order_id,
                                   product_id=product_id,
                                   product_name=product_detail.name,
                                   price=product_detail.sale_price,
                                   quantity=order_quantity)

            add_items_ordered = await customer_controller.add_items_to_temp_order(customer_id=user.customer_id,
                                                                                  order_id=temp_order.order_id,
                                                                                  order_item=order_item)
        else:
            # TODO - redirect to customer details captcha
            flash(message="Please Enter Customer Details", category="danger")
            return redirect(url_for('cart.get_orders'))

    flash(message="Order Successfully Captured", category="success")
    return redirect(url_for('cart.get_cart'))


@cart_route.post("/customer/capture")
@login_required
async def capture_customer_details(user: User):
    """

    :param user:
    :return:
    """
    customer_details = CustomerDetails(**request.form, uid=user.uid, customer_id=user.customer_id)
    customer_details_ = await customer_controller.add_customer_details(customer_details=customer_details)
    flash(message="Successfully Captured Customer Details")
    return redirect(url_for('cart.get_orders'))
