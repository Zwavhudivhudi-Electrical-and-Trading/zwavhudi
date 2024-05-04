from flask import Blueprint, render_template, url_for

from src.database.models.products import Product
from src.authentication import user_details
from src.database.models.users import User

cart_route = Blueprint('cart', __name__)


@cart_route.get("/shopping-cart")
@user_details
async def get_cart(user: User | None):
    social_url = url_for('cart.get_cart', _external=True)

    products_list: list[Product] = [
        Product(product_id=1, name="Domestos", description="Keep your toilets clean at all times",
                img_link="images/cleaning.jpg", price=100, category_id=1),
        Product(product_id=2, name="Grease Remover", description="Removes Grease with ease",
                img_link="images/cleaning_2.jpg", price=150, category_id=2),
        Product(product_id=3, name="Window Cleaner", description="Great for Sparkling Windows",
                img_link="images/cleaning_3.jpg", price=200, category_id=1),

        Product(product_id=1, name="Domestos", description="Keep your toilets clean at all times",
                img_link="images/cleaning.jpg", price=100, category_id=1),
        Product(product_id=2, name="Grease Remover", description="Removes Grease with ease",
                img_link="images/cleaning_2.jpg", price=150, category_id=2),
        Product(product_id=3, name="Window Cleaner", description="Great for Sparkling Windows",
                img_link="images/cleaning_3.jpg", price=200, category_id=1),

        Product(product_id=1, name="Domestos", description="Keep your toilets clean at all times",
                img_link="images/cleaning.jpg", price=100, category_id=1),
        Product(product_id=2, name="Grease Remover", description="Removes Grease with ease",
                img_link="images/cleaning_2.jpg", price=150, category_id=2),
        Product(product_id=3, name="Window Cleaner", description="Great for Sparkling Windows",
                img_link="images/cleaning_3.jpg", price=200, category_id=1),
        # Add more test data as needed
    ]
    context = dict(user=user, social_url=social_url, products_list=products_list)
    return render_template('cart/cart.html', **context)


@cart_route.get("/orders")
@user_details
async def get_orders(user: User | None):
    social_url = url_for('cart.get_orders', _external=True)
    context = dict(user=user, social_url=social_url)
    return render_template('orders/orders.html', **context)