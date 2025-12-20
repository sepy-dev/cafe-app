from domain.entities.order import Order
from infrastructure.database.session import SessionLocal
from infrastructure.database.repositories.order_repository_sqlalchemy import (
    OrderRepositorySQLAlchemy
)

class OrderService:
    def __init__(self):
        self.order = Order()
        self.session = SessionLocal()
        self.repo = OrderRepositorySQLAlchemy(self.session)

    def add_item(self, name: str, price: int, quantity: int = 1):
        self.order.add_item(name, price, quantity)

    def remove_item(self, name: str):
        self.order.remove_item(name)

    def change_quantity(self, name: str, quantity: int):
        self.order.change_quantity(name, quantity)

    def apply_discount(self, amount: int):
        self.order.apply_discount(amount)

    def get_items(self):
        return self.order.get_items()

    def get_total_price(self) -> int:
        return self.order.total_price()

    def close_order(self):
        self.order.close()

    def close_and_save(self) -> int:
        self.order.close()
        order_id = self.repo.save(self.order)
        self.clear()
        return order_id    

    def clear(self):
        self.order = Order()
