from sqlalchemy.orm import Session

from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from domain.repositories.order_repository import OrderRepository
from domain.entities.enums import OrderStatus

from infrastructure.database.models.order_model import OrderModel
from infrastructure.database.models.order_item_model import OrderItemModel


class OrderRepositorySQLAlchemy(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> int:
        order_model = OrderModel(
            status=order.status.value,
            discount=order.discount
        )
        self.session.add(order_model)
        self.session.flush()  # گرفتن ID

        for item in order.get_items():
            item_model = OrderItemModel(
                order_id=order_model.id,
                product_name=item.name,
                unit_price=item.unit_price,
                quantity=item.quantity
            )
            self.session.add(item_model)

        self.session.commit()
        return order_model.id

    def get_by_id(self, order_id: int) -> Order:
        order_model = self.session.get(OrderModel, order_id)

        if not order_model:
            raise Exception("Order not found")

        order = Order()
        order.discount = order_model.discount
        order.status = OrderStatus(order_model.status)

        items = (
            self.session.query(OrderItemModel)
            .filter_by(order_id=order_id)
            .all()
        )

        for i in items:
            order.add_item(
                name=i.product_name,
                price=i.unit_price,
                quantity=i.quantity
            )

        return order
