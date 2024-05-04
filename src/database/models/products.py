from pydantic import BaseModel


class Category(BaseModel):
    """Product category"""
    category_id: int
    name: str
    description: str


class Product(BaseModel):
    """Product being sold"""
    product_id: int
    name: str
    description: str
    price: int
    category_id: int


class Inventory(BaseModel):
    """Inventory of products"""

    product_id: int
    quantity: int

