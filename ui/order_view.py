from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
)
from ui.widgets.keypad_widget import KeypadWidget
from application.order_service import OrderService


class OrderView(QWidget):
    def __init__(self):
        super().__init__()

        self.order_service = OrderService()

        layout = QVBoxLayout(self)

        title = QLabel("سفارش جاری")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        self.order_list = QListWidget()
        self.total_label = QLabel("جمع کل: 0 تومان")
        self.total_label.setStyleSheet("font-size:16px; font-weight:bold;")

        self.keypad = KeypadWidget()
        self.keypad.value_entered.connect(self.add_test_item)

        layout.addWidget(title)
        layout.addWidget(self.order_list, 1)
        layout.addWidget(self.total_label)
        layout.addWidget(self.keypad)

    def add_test_item(self, qty: int):
        """
        فعلاً تستی:
        با وارد کردن عدد → قهوه اضافه میشه
        بعداً منو وصل می‌کنیم
        """
        self.order_service.add_item(
            name="قهوه",
            price=50000,
            quantity=qty
        )
        self.refresh_ui()

    def refresh_ui(self):
        self.order_list.clear()

        for item in self.order_service.get_items():
            text = f"{item.name}  x{item.quantity}  |  {item.price * item.quantity} تومان"
            self.order_list.addItem(QListWidgetItem(text))

        self.total_label.setText(
            f"جمع کل: {self.order_service.get_total_price()} تومان"
        )
