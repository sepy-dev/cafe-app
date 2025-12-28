from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpinBox
from PySide6.QtCore import Signal


class OrderItemWidget(QWidget):
    quantity_changed = Signal(str, int)  # name, new_quantity

    def __init__(self, name: str, qty: int, price: int):
        super().__init__()
        self.setProperty("class", "order-item")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        # نام محصول
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #1976D2;
                min-width: 150px;
            }
        """)
        layout.addWidget(self.lbl_name)

        # کنترل تعداد
        qty_widget = QWidget()
        qty_layout = QVBoxLayout(qty_widget)
        qty_layout.setContentsMargins(0, 0, 0, 0)
        qty_layout.setSpacing(2)

        qty_label = QLabel("تعداد")
        qty_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
        qty_layout.addWidget(qty_label)

        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(99)
        self.qty_spin.setValue(qty)
        self.qty_spin.setMaximumWidth(70)
        self.qty_spin.setStyleSheet("""
            QSpinBox {
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                padding: 4px 8px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                background-color: #F5F5F5;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #E0E0E0;
            }
        """)
        self.qty_spin.valueChanged.connect(self.on_quantity_changed)
        qty_layout.addWidget(self.qty_spin)

        layout.addWidget(qty_widget)

        # قیمت واحد
        unit_price = price // qty  # محاسبه قیمت واحد
        unit_widget = QWidget()
        unit_layout = QVBoxLayout(unit_widget)
        unit_layout.setContentsMargins(0, 0, 0, 0)
        unit_layout.setSpacing(2)

        unit_label = QLabel("قیمت واحد")
        unit_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
        unit_layout.addWidget(unit_label)

        self.lbl_unit_price = QLabel(f"{unit_price:,} تومان")
        self.lbl_unit_price.setStyleSheet("""
            QLabel {
                color: #FF6F00;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        unit_layout.addWidget(self.lbl_unit_price)

        layout.addWidget(unit_widget)

        # قیمت کل
        total_widget = QWidget()
        total_layout = QVBoxLayout(total_widget)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_layout.setSpacing(2)

        total_label = QLabel("مجموع")
        total_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
        total_layout.addWidget(total_label)

        self.lbl_price = QLabel(f"{price:,} تومان")
        self.lbl_price.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #4CAF50;
                font-size: 14px;
            }
        """)
        total_layout.addWidget(self.lbl_price)

        layout.addWidget(total_widget)

        layout.addStretch()

        # دکمه حذف
        self.btn_remove = QPushButton("🗑️")
        self.btn_remove.setToolTip("حذف آیتم")
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
        """)
        self.btn_remove.setMaximumWidth(50)
        layout.addWidget(self.btn_remove)

    def on_quantity_changed(self, new_qty: int):
        """وقتی تعداد تغییر کرد"""
        # به‌روزرسانی قیمت کل
        unit_price = int(self.lbl_unit_price.text().split(": ")[1].replace(",", "").replace(" تومان", ""))
        total_price = unit_price * new_qty
        self.lbl_price.setText(f"مجموع: {total_price:,} تومان")

        # ارسال سیگنال
        self.quantity_changed.emit(self.lbl_name.text(), new_qty)
