from dataclasses import dataclass
from typing import List


@dataclass
class OrderItemDTO:
    name: str
    quantity: int
    price: int


class OrderService:
    def __init__(self):
        self.items: List[OrderItemDTO] = []

    def add_item(self, name: str, price: int, quantity: int = 1):
        for item in self.items:
            if item.name == name:
                item.quantity += quantity
                return
        self.items.append(OrderItemDTO(name, quantity, price))

    def remove_item(self, name: str):
        self.items = [i for i in self.items if i.name != name]

    def get_items(self) -> List[OrderItemDTO]:
        return self.items

    def get_total_price(self) -> int:
        return sum(i.price * i.quantity for i in self.items)

    def clear(self):
        self.items.clear()
