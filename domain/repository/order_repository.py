from abc import ABC, abstractmethod
from typing import List
from domain.entities.order_item import OrderItem
from domain.entities.order import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> int:
        """ذخیره سفارش کامل و برگرداندن ID"""
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        """دریافت سفارش بر اساس ID"""
        pass

    @abstractmethod
    def add(self, order_item: OrderItem) -> None:
        pass

    @abstractmethod
    def list(self) -> List[OrderItem]:
        pass
