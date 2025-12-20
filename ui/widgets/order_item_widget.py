from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class OrderItemWidget(QWidget):
    def __init__(self, name: str, qty: int, price: int):
        super().__init__()

        layout = QHBoxLayout(self)

        self.lbl_name = QLabel(name)
        self.lbl_qty = QLabel(f"x{qty}")
        self.lbl_price = QLabel(f"{price} تومان")
        self.btn_remove = QPushButton("❌")

        layout.addWidget(self.lbl_name)
        layout.addWidget(self.lbl_qty)
        layout.addWidget(self.lbl_price)
        layout.addWidget(self.btn_remove)
