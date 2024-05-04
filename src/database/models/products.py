from enum import Enum
from datetime import date as Date
from datetime import datetime

from pydantic import BaseModel


class InventoryEntryReasons(Enum):
    ADD = "Addition"
    SUBTRACT = "Subtraction"
    SALE = "Sale"  # Added SALE reason
    BREAKAGE = "Breakage"
    STOCK = "Stock"
    REFUND = "Refund"




class InventoryEntries(BaseModel):
    """Inventory of products"""
    entry_id: str
    product_id: int
    amount: int
    entry_datetime: str
    reason: str
    price: int

    @property
    def real_amount(self) -> int:
        if self.reason == InventoryEntryReasons.ADD.value:
            return self.amount
        elif self.reason == InventoryEntryReasons.STOCK.value:
            return self.amount
        elif self.reason == InventoryEntryReasons.SUBTRACT.value:
            return self.amount * -1
        elif self.reason == InventoryEntryReasons.SALE.value:
            return self.amount * -1
        elif self.reason == InventoryEntryReasons.REFUND.value:
            return self.amount

    @property
    def stock_value(self) -> int:
        return self.real_amount * self.price

    @property
    def is_stock_in(self):
        return self.reason in [InventoryEntryReasons.REFUND.value, InventoryEntryReasons.STOCK.value,
                               InventoryEntryReasons.ADD.value]

    @property
    def entry_date(self) -> Date:
        # Convert entry_datetime string to a datetime object
        entry_datetime_obj = datetime.strptime(self.entry_datetime, "%Y-%m-%d %H:%M:%S")
        # Format the datetime object to a date string
        return entry_datetime_obj


class Product(BaseModel):
    """Product being sold"""
    category_id: int
    product_id: int
    name: str
    description: str
    img_link: str
    price: int
    inventory_entries: list[InventoryEntries]

    @property
    def total_inventory(self):
        return sum([entry.real_amount for entry in self.inventory_entries])

    @property
    def stock_value(self):
        return sum([entry.stock_value for entry in self.inventory_entries])

    def total_stock_count_in_date_range(self, start_date: Date, stop_date: Date):
        """

        :param start_date:
        :param stop_date:
        :return:
        """
        return sum(
            entry.real_amount for entry in self.inventory_entries
            if start_date <= entry.entry_date <= stop_date
        )

    def total_stock_in_value_in_date_range(self, start_date: Date, stop_date: Date):
        """

        :param start_date:
        :param stop_date:
        :return:
        """
        return sum(
            entry.stock_value for entry in self.inventory_entries
            if (start_date <= entry.entry_date <= stop_date) and entry.is_stock_in
        )

    def total_stock_out_value_in_date_range(self, start_date: Date, stop_date: Date):
        """

        :param start_date:
        :param stop_date:
        :return:
        """
        return sum(
            entry.stock_value for entry in self.inventory_entries
            if (start_date <= entry.entry_date <= stop_date) and not entry.is_stock_in
        )


class Category(BaseModel):
    """Product category"""
    category_id: int
    name: str
    description: str
    products_list: list[Product]
