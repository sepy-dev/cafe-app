# domain/entities/order.py
from domain.entities.order_item import OrderItem
class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items

    def total_price(self) -> int:
        return sum(item.total_price() for item in self.items)
