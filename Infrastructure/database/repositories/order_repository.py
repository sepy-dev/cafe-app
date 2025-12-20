from abc import ABC, abstractmethod
from domain.entities.order import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> int:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass
