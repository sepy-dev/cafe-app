from abc import ABC, abstractmethod
from typing import List
from domain.entities.order_item import OrderItem


class OrderRepository(ABC):

    @abstractmethod
    def add(self, order_item: OrderItem) -> None:
        pass

    @abstractmethod
    def list(self) -> List[OrderItem]:
        pass
