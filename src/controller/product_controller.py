from flask import Flask

from src.database.sql.products import ProductsORM
from src.database.models.products import Product
from src.controller import Controllers, error_handler


class ProductController(Controllers):
    def __init__(self):
        super().__init__()

    def init_app(self, app: Flask):
        super().init_app(app=app)


    async def get_product(self, product_id: str) -> Product | None:
        """

        :param product_id:
        :return:
        """
        with self.get_session() as session:
            product_orm = session.query(ProductsORM).filter_by(product_id=product_id).first()
            if isinstance(product_orm, ProductsORM):
                return Product(**product_orm.to_dict())
            return None