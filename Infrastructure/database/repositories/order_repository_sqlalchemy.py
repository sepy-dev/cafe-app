from sqlalchemy.orm import Session

from domain.entities.order import Order
from domain.entities.order_item import OrderItem
from .order_repository import OrderRepository
from domain.entities.enums import OrderStatus

from infrastructure.database.models.order_model import OrderModel
from infrastructure.database.models.order_item_model import OrderItemModel


class OrderRepositorySQLAlchemy(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> int:
        order_model = OrderModel(
            table_number=order.table_number,
            status=order.status.value,
            discount=order.discount.amount
        )
        self.session.add(order_model)
        self.session.flush()  # گرفتن ID

        for item in order.get_items():
            item_model = OrderItemModel(
                order_id=order_model.id,
                product_name=item.name,
                unit_price=item.unit_price.amount,
                quantity=item.quantity
            )
            self.session.add(item_model)

        self.session.commit()
        return order_model.id

    def get_by_id(self, order_id: int) -> Order:
        from domain.value_objects.money import Money

        order_model = self.session.get(OrderModel, order_id)

        if not order_model:
            raise Exception("Order not found")

        order = Order(table_number=order_model.table_number)
        order.discount = Money(order_model.discount)
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
    
    def get_open_order_by_table(self, table_number: int) -> Order:
        """Get open order for a specific table"""
        from domain.value_objects.money import Money
        
        # Find open order for this table
        order_model = (
            self.session.query(OrderModel)
            .filter_by(table_number=table_number, status="open")
            .order_by(OrderModel.created_at.desc())
            .first()
        )
        
        if not order_model:
            return None
        
        # Convert to domain Order
        order = Order(table_number=order_model.table_number)
        order.discount = Money(order_model.discount)
        # Convert lowercase status to uppercase for enum
        status_str = order_model.status.upper() if order_model.status else "OPEN"
        try:
            order.status = OrderStatus[status_str]
        except KeyError:
            order.status = OrderStatus.OPEN
        
        # Load order items
        items = (
            self.session.query(OrderItemModel)
            .filter_by(order_id=order_model.id)
            .all()
        )
        
        for item_model in items:
            order.add_item(
                name=item_model.product_name,
                price=item_model.unit_price,
                quantity=item_model.quantity
            )
        
        return order
    
    def update_order(self, order_id: int, order: Order) -> None:
        """Update existing order"""
        order_model = self.session.get(OrderModel, order_id)
        if not order_model:
            raise Exception("Order not found")
        
        # Update order fields
        order_model.status = order.status.value
        order_model.discount = order.discount.amount
        
        # Update items - remove old items and add new ones
        self.session.query(OrderItemModel).filter_by(order_id=order_id).delete()
        
        for item in order.get_items():
            item_model = OrderItemModel(
                order_id=order_id,
                product_name=item.name,
                unit_price=item.unit_price.amount,
                quantity=item.quantity
            )
            self.session.add(item_model)
        
        self.session.commit()
    
    def add(self, order_item: OrderItem) -> None:
        self.session.add(order_item)
        self.session.commit()

    def list(self):
        return self.session.query(OrderItem).all()