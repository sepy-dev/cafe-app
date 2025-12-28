from domain.entities.order import Order
from infrastructure.database.session import SessionLocal
from infrastructure.database.repositories.order_repository_sqlalchemy import (
    OrderRepositorySQLAlchemy
)
from infrastructure.printer.receipt_printer import ReceiptPrinter
from domain.entities.order_item import OrderItem
from domain.value_objects.money import Money


class OrderService:
    def __init__(self):
        self.order = Order()
        self.session = SessionLocal()
        self.repo = OrderRepositorySQLAlchemy(self.session)
        self.printer = ReceiptPrinter()

    def add_item(self, name: str, price: int, quantity: int = 1):
        try:
            self.order.add_item(name, price, quantity)
        except ValueError as e:
            raise ValueError(f"خطا در افزودن آیتم: {e}")

    def remove_item(self, name: str):
        try:
            self.order.remove_item(name)
        except ValueError as e:
            raise ValueError(f"خطا در حذف آیتم: {e}")

    def change_quantity(self, name: str, quantity: int):
        try:
            self.order.change_quantity(name, quantity)
        except ValueError as e:
            raise ValueError(f"خطا در تغییر تعداد: {e}")

    def apply_discount(self, amount: int):
        try:
            self.order.apply_discount(amount)
        except ValueError as e:
            raise ValueError(f"خطا در اعمال تخفیف: {e}")

    def get_items(self):
        return self.order.get_items()

    def get_total_price(self) -> Money:
        return self.order.total_price()

    def get_subtotal(self) -> Money:
        """مجموع قیمت قبل از تخفیف"""
        return Money(sum(item.total_price().amount for item in self.order.items))

    def get_discount(self) -> Money:
        return self.order.discount

    def close_order(self):
        try:
            self.order.close()
        except ValueError as e:
            raise ValueError(f"خطا در بستن سفارش: {e}")

    def close_and_save(self) -> int:
        try:
            self.order.close()
            order_id = self.repo.save(self.order)
            self.clear()
            return order_id
        except Exception as e:
            raise ValueError(f"خطا در ذخیره سفارش: {e}")

    def clear(self):
        self.order = Order()

    def set_table(self, table_number: int):
        """تعیین شماره میز"""
        if self.order.status != Order().status:  # اگر سفارش شروع شده
            raise ValueError("نمی‌توان شماره میز را تغییر داد")
        self.order.table_number = table_number

    def get_table_number(self) -> int:
        return self.order.table_number

    def print_receipt(self, order_id: int) -> str:
        """چاپ فاکتور سفارش"""
        try:
            # اگر سفارش فعلی است، مستقیم چاپ کن
            if self.order.status.value == "CLOSED":
                return self.printer.print_receipt(self.order, order_id)
            else:
                # اگر سفارش ذخیره شده است، از دیتابیس بخوان
                saved_order = self.repo.get_by_id(order_id)
                return self.printer.print_receipt(saved_order, order_id)
        except Exception as e:
            raise ValueError(f"خطا در چاپ فاکتور: {e}")

    def print_test_receipt(self):
        """چاپ فاکتور تست"""
        self.printer.print_test_receipt()
