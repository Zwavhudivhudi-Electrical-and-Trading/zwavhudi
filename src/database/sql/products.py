from datetime import datetime

from sqlalchemy.orm import relationship

from src.database.constants import ID_LEN, NAME_LEN
from src.database.sql import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, inspect, ForeignKey



class ProductsORM(Base):
    __tablename__ = "products"
