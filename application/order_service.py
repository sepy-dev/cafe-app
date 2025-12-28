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
        self.orders = {}  # table_number -> Order object
        self.current_table = None
        self.session = SessionLocal()
        self.repo = OrderRepositorySQLAlchemy(self.session)
        self.printer = ReceiptPrinter()

    @property
    def current_order(self):
        """دریافت سفارش فعلی بر اساس میز انتخاب شده"""
        if self.current_table is None:
            return None
        if self.current_table not in self.orders:
            self.orders[self.current_table] = Order(table_number=self.current_table)
        return self.orders[self.current_table]

    def add_item(self, name: str, price: int, quantity: int = 1):
        if self.current_order is None:
            raise ValueError("لطفاً ابتدا میز را انتخاب کنید")
        try:
            self.current_order.add_item(name, price, quantity)
        except ValueError as e:
            raise ValueError(f"خطا در افزودن آیتم: {e}")

    def remove_item(self, name: str):
        if self.current_order is None:
            raise ValueError("هیچ سفارشی انتخاب نشده است")
        try:
            self.current_order.remove_item(name)
        except ValueError as e:
            raise ValueError(f"خطا در حذف آیتم: {e}")

    def change_quantity(self, name: str, quantity: int):
        if self.current_order is None:
            raise ValueError("هیچ سفارشی انتخاب نشده است")
        try:
            self.current_order.change_quantity(name, quantity)
        except ValueError as e:
            raise ValueError(f"خطا در تغییر تعداد: {e}")

    def apply_discount(self, amount: int):
        if self.current_order is None:
            raise ValueError("هیچ سفارشی انتخاب نشده است")
        try:
            self.current_order.apply_discount(amount)
        except ValueError as e:
            raise ValueError(f"خطا در اعمال تخفیف: {e}")

    def get_items(self):
        if self.current_order is None:
            return []
        return self.current_order.get_items()

    def get_total_price(self) -> Money:
        if self.current_order is None:
            return Money(0)
        return self.current_order.total_price()

    def get_subtotal(self) -> Money:
        """مجموع قیمت قبل از تخفیف"""
        if self.current_order is None:
            return Money(0)
        return Money(sum(item.total_price().amount for item in self.current_order.items))

    def get_discount(self) -> Money:
        if self.current_order is None:
            return Money(0)
        return self.current_order.discount

    def close_order(self):
        if self.current_order is None:
            raise ValueError("هیچ سفارشی انتخاب نشده است")
        try:
            self.current_order.close()
        except ValueError as e:
            raise ValueError(f"خطا در بستن سفارش: {e}")

    def close_and_save(self) -> int:
        if self.current_order is None:
            raise ValueError("هیچ سفارشی انتخاب نشده است")
        try:
            self.current_order.close()
            order_id = self.repo.save(self.current_order)
            # حذف سفارش بسته شده از حافظه
            if self.current_table in self.orders:
                del self.orders[self.current_table]
            return order_id
        except Exception as e:
            raise ValueError(f"خطا در ذخیره سفارش: {e}")

    def clear_current_order(self):
        """پاک کردن سفارش فعلی"""
        if self.current_table and self.current_table in self.orders:
            del self.orders[self.current_table]

    def set_table(self, table_number: int):
        """تعیین شماره میز فعلی"""
        self.current_table = table_number

    def get_table_number(self) -> int:
        """دریافت شماره میز فعلی"""
        return self.current_table if self.current_table is not None else 0

    def print_receipt(self, order_id: int) -> str:
        """چاپ فاکتور سفارش"""
        try:
            # از دیتابیس سفارش را بخوان
            saved_order = self.repo.get_by_id(order_id)
            return self.printer.print_receipt(saved_order, order_id)
        except Exception as e:
            raise ValueError(f"خطا در چاپ فاکتور: {e}")

    def print_test_receipt(self):
        """چاپ فاکتور تست"""
        self.printer.print_test_receipt()
