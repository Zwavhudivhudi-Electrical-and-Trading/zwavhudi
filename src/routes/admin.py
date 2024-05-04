from flask import Blueprint, render_template, url_for

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
    context = dict(user=user, products_list=products_list)
    return render_template('admin/products/products.html', **context)


@admin_route.get('/admin/messages')
@login_required
async def get_messages(user: User):
    pass
