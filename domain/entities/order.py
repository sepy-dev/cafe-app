# domain/entities/order.py
from domain.entities.order_item import OrderItem
from domain.entities.enums import OrderStatus
from domain.value_objects.money import Money

class Order:
    def __init__(self, table_number: int = None):
        self.items = []
        self.status = OrderStatus.OPEN
        self.discount = Money(0)
        self.table_number = table_number

    def add_item(self, name: str, price: int, quantity: int):
        # بررسی قوانین بیزنسی
        if self.status != OrderStatus.OPEN:
            raise ValueError("نمی‌توان به سفارش بسته شده آیتم اضافه کرد")

        if quantity <= 0:
            raise ValueError("تعداد باید مثبت باشد")

        # بررسی آیا آیتم مشابه وجود دارد
        for item in self.items:
            if item.name == name:
                item.quantity += quantity
                return

        # ایجاد آیتم جدید
        item = OrderItem(name, price, quantity)
        self.items.append(item)

    def remove_item(self, name: str):
        if self.status != OrderStatus.OPEN:
            raise ValueError("نمی‌توان از سفارش بسته شده آیتم حذف کرد")

        self.items = [item for item in self.items if item.name != name]

    def change_quantity(self, name: str, quantity: int):
        if self.status != OrderStatus.OPEN:
            raise ValueError("نمی‌توان سفارش بسته شده را تغییر داد")

        if quantity <= 0:
            self.remove_item(name)
            return

        for item in self.items:
            if item.name == name:
                item.quantity = quantity
                return

        raise ValueError(f"آیتم {name} در سفارش یافت نشد")

    def apply_discount(self, amount: int):
        if self.status != OrderStatus.OPEN:
            raise ValueError("نمی‌توان به سفارش بسته شده تخفیف اعمال کرد")

        if amount < 0 or amount > self.total_price().amount:
            raise ValueError("مبلغ تخفیف نامعتبر است")

        self.discount = Money(amount)

    def get_items(self):
        return self.items.copy()

    def total_price(self) -> Money:
        subtotal = Money(0)
        for item in self.items:
            subtotal += item.total_price()
        return Money(max(0, subtotal.amount - self.discount.amount))

    def close(self):
        if self.status != OrderStatus.OPEN:
            raise ValueError("سفارش قبلاً بسته شده است")

        if not self.items:
            raise ValueError("نمی‌توان سفارش خالی را بست")

        self.status = OrderStatus.CLOSED
