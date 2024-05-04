from flask import Flask

from src.database.models.products import Product, InventoryEntries, InventoryEntryReasons


def register_routes(app: Flask):
    from src.routes.home import home_route
    from src.routes.auth import auth_route
    from src.routes.cart import cart_route
    from src.routes.admin import admin_route

    routes = [auth_route, home_route, cart_route, admin_route]
    for route in routes:
        app.register_blueprint(route)



def product_test_values() -> list[Product]:
    return [
        Product(
            product_id=1,
            name="Domestos",
            description="Keep your toilets clean at all times",
            img_link="images/cleaning.jpg",
            price=100,
            category_id=1,
            inventory_entries=[
                InventoryEntries(entry_id='1', product_id=1, amount=10, entry_datetime='2024-05-01 10:00:00',
                                 reason=InventoryEntryReasons.ADD.value, price=200),
                InventoryEntries(entry_id='2', product_id=1, amount=5, entry_datetime='2024-05-02 12:00:00',
                                 reason=InventoryEntryReasons.SALE.value, price=200),
                InventoryEntries(entry_id='3', product_id=1, amount=2, entry_datetime='2024-05-03 14:00:00',
                                 reason=InventoryEntryReasons.ADD.value, price=200),
            ]
        ),
        Product(
            product_id=2,
            name="Grease Remover",
            description="Removes Grease with ease",
            img_link="images/cleaning_2.jpg",
            price=150,
            category_id=2,
            inventory_entries=[
                InventoryEntries(entry_id='4', product_id=2, amount=8, entry_datetime='2024-05-01 09:00:00',
                                 reason=InventoryEntryReasons.ADD.value, price=200),
                InventoryEntries(entry_id='5', product_id=2, amount=3, entry_datetime='2024-05-02 10:00:00',
                                 reason=InventoryEntryReasons.SALE.value, price=200),
                InventoryEntries(entry_id='6', product_id=2, amount=4, entry_datetime='2024-05-03 11:00:00',
                                 reason=InventoryEntryReasons.STOCK.value, price=200),
            ]
        ),
        Product(
            product_id=3,
            name="Window Cleaner",
            description="Great for Sparkling Windows",
            img_link="images/cleaning_3.jpg",
            price=200,
            category_id=1,
            inventory_entries=[
                InventoryEntries(entry_id='7', product_id=3, amount=12, entry_datetime='2024-05-01 08:00:00',
                                 reason=InventoryEntryReasons.ADD.value, price=200),
                InventoryEntries(entry_id='8', product_id=3, amount=6, entry_datetime='2024-05-02 09:00:00',
                                 reason=InventoryEntryReasons.SALE.value, price=200),
                InventoryEntries(entry_id='9', product_id=3, amount=5, entry_datetime='2024-05-03 10:00:00',
                                 reason=InventoryEntryReasons.STOCK.value, price=200),
            ]
        )
    ]
