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
    img_link: str
    price: int
    category_id: int


class InventoryEntries(BaseModel):
    """Inventory of products"""
    entry_id: str
    product_id: int
    add: int
    subtract: int
    entry_datetime: str
    reason: str


