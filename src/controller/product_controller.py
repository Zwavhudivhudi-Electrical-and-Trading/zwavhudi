import os

from flask import Flask
from werkzeug.utils import secure_filename

from src.database.sql.products import ProductsORM, CategoryORM
from src.database.models.products import Product, Category
from src.controller import Controllers, error_handler
from src.utils import static_folder


class ProductController(Controllers):
    def __init__(self):
        super().__init__()

    def init_app(self, app: Flask):
        super().init_app(app=app)
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

    import os

    @staticmethod
    async def create_category_link(category_name: str, extension: str) -> str | None:
        """
        Create a category image link based on the category name and extension.
        :param category_name: The name of the category
        :param extension: The file extension of the image
        :return: The category image link
        """
        category_name = category_name.lower().strip()
        extension = extension.lower().strip()

        # Sanitize extension
        if "." in extension:
            extension = extension.split(".")[1]
        extension = extension.lower().strip()

        # Obtain the path to the static folder
        static_folder_path = static_folder()

        # Construct the directory path for the category
        category_dir = os.path.join("images", "inventory", category_name)

        # Create the category directory if it doesn't exist
        os.makedirs(f"{static_folder()}/{category_dir}", exist_ok=True)

        # Construct the image link
        image_link = os.path.join(f"/{category_dir}/{category_name}.{extension}")

        # Return the image link
        return image_link.replace("\\", "/")  # Replace backslashes for Windows compatibility

    @staticmethod
    async def create_product_link(category_name: str, product_name: str, extension: str) -> str | None:
        """

        :param category_name:
        :param product_name:
        :param extension:
        :return:
        """
        category_name = category_name.lower().strip()
        product_name = product_name.lower().strip()
        if "." in extension:
            extension = extension.split(".")[1]
        extension = extension.lower().strip()

        if category_name and product_name and extension:
            return os.path.join(f"{static_folder()}images/inventory/{category_name}/{product_name}.{extension}")
        else:
            return None

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

    async def get_products(self) -> list[Product]:
        """

        :return:
        """
        with self.get_session() as session:
            products_list_orm = session.query(ProductsORM).all()
            return [Product(**product_orm.to_dict()) for product_orm in products_list_orm
                    if isinstance(product_orm, ProductsORM)]

    async def get_categories(self) -> list[Category]:
        """

        :return:
        """
        with self.get_session() as session:
            category_list_orm = session.query(CategoryORM).all()
            return [Category(**category_orm.to_dict()) for category_orm in category_list_orm
                    if isinstance(category_orm, CategoryORM)]

    async def add_category(self, category_detail: Category) -> Category:
        """

        :return:
        """
        with self.get_session() as session:
            name = category_detail.name.lower().strip()
            category_orm = session.query(CategoryORM).filter_by(name=name).first()

            if isinstance(category_orm, CategoryORM):
                category_orm.name = category_detail.name
                category_orm.description = category_detail.description
                category_orm.products_list = category_detail.products_list
                category_orm.img_link = category_detail.img_link

            else:
                category_orm = CategoryORM(**category_detail.dict())
                session.add(category_orm)

            session.commit()

            return category_detail

    async def save_category_image(self, category_name: str, image) -> str:
        """
            will return image link
        :return:
        """
        filename = secure_filename(image.filename)
        ext_list = filename.split(".")
        extension = ext_list[-1]
        extension = extension.lower().strip()

        if extension not in self.allowed_extensions:
            return None

        destination_image_path = await self.create_category_link(category_name=category_name, extension=extension)
        image.save(f"{static_folder()}destination_image_path")
        return destination_image_path





"""

<img alt="Tools" src="H:/projects/source/dreamland/src/utils/../../static/images/inventory/tools/tools.png" class="img-fluid">

"""
