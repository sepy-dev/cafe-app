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
            # Check if there's an open order in database for this table
            db_order = self.repo.get_open_order_by_table(self.current_table)
            if db_order:
                # Load existing order from database
                self.orders[self.current_table] = db_order
            else:
                # Create new order
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
            
            # Check if order already exists in database (from web)
            from infrastructure.database.models.order_model import OrderModel
            order_model = (
                self.session.query(OrderModel)
                .filter_by(table_number=self.current_table, status="open")
                .order_by(OrderModel.created_at.desc())
                .first()
            )
            
            if order_model:
                # Update existing order
                self.repo.update_order(order_model.id, self.current_order)
                order_id = order_model.id
            else:
                # Save as new order
                order_id = self.repo.save(self.current_order)
            
            # حذف سفارش بسته شده از حافظه
            if self.current_table in self.orders:
                del self.orders[self.current_table]
            return order_id
        except Exception as e:
            raise ValueError(f"خطا در ذخیره سفارش: {str(e)}")

    def clear_current_order(self):
        """پاک کردن سفارش فعلی"""
        if self.current_table and self.current_table in self.orders:
            del self.orders[self.current_table]

    def set_table(self, table_number: int):
        """تعیین شماره میز فعلی و بارگذاری سفارش باز از دیتابیس"""
        self.current_table = table_number
        
        # Clear current order from memory to force reload
        if table_number in self.orders:
            del self.orders[table_number]
        
        # This will trigger current_order property which loads from DB if exists
        # Accessing current_order will load from DB or create new
        _ = self.current_order

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
