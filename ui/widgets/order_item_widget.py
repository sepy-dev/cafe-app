from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpinBox
from PySide6.QtCore import Signal


class OrderItemWidget(QWidget):
    quantity_changed = Signal(str, int)  # name, new_quantity

    def __init__(self, name: str, qty: int, price: int):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # نام محصول
        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.lbl_name.setMinimumWidth(150)
        layout.addWidget(self.lbl_name)

        # کنترل تعداد
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("تعداد:"))

        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(99)
        self.qty_spin.setValue(qty)
        self.qty_spin.setMaximumWidth(60)
        self.qty_spin.valueChanged.connect(self.on_quantity_changed)

        qty_layout.addWidget(self.qty_spin)
        layout.addLayout(qty_layout)

        # قیمت واحد
        unit_price = price // qty  # محاسبه قیمت واحد
        self.lbl_unit_price = QLabel(f"قیمت واحد: {unit_price:,} تومان")
        self.lbl_unit_price.setStyleSheet("color: #666;")
        layout.addWidget(self.lbl_unit_price)

        # قیمت کل
        self.lbl_price = QLabel(f"مجموع: {price:,} تومان")
        self.lbl_price.setStyleSheet("font-weight: bold; color: #2E7D32;")
        layout.addWidget(self.lbl_price)

        # دکمه حذف
        self.btn_remove = QPushButton("❌ حذف")
        self.btn_remove.setStyleSheet("color: #D32F2F;")
        self.btn_remove.setMaximumWidth(80)
        layout.addWidget(self.btn_remove)

        layout.addStretch()

    def on_quantity_changed(self, new_qty: int):
        """وقتی تعداد تغییر کرد"""
        # به‌روزرسانی قیمت کل
        unit_price = int(self.lbl_unit_price.text().split(": ")[1].replace(",", "").replace(" تومان", ""))
        total_price = unit_price * new_qty
        self.lbl_price.setText(f"مجموع: {total_price:,} تومان")

        # ارسال سیگنال
        self.quantity_changed.emit(self.lbl_name.text(), new_qty)
