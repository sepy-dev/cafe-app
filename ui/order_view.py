#order_view
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QHBoxLayout, QPushButton, QLineEdit, QMessageBox, QSpinBox,
    QGroupBox, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
from ui.widgets.keypad_widget import KeypadWidget
from ui.widgets.order_item_widget import OrderItemWidget
from application.order_service import OrderService


class OrderView(QWidget):
    def __init__(self):
        super().__init__()

        self.order_service = OrderService()

        layout = QVBoxLayout(self)

        # عنوان
        title = QLabel("سفارش جاری")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        # انتخاب میز
        table_group = QGroupBox("اطلاعات سفارش")
        table_layout = QFormLayout(table_group)

        self.table_combo = QComboBox()
        self.table_combo.addItems([f"میز {i}" for i in range(1, 21)])  # ۲۰ میز
        self.table_combo.addItem("بیرون بر")  # گزینه بیرون بر
        self.table_combo.currentIndexChanged.connect(self.on_table_changed)

        table_layout.addRow("میز:", self.table_combo)
        layout.addWidget(table_group)

        # لیست آیتم‌های سفارش
        self.order_list = QListWidget()
        self.order_list.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.order_list, 1)

        # اطلاعات مالی
        financial_group = QGroupBox("اطلاعات مالی")
        financial_layout = QFormLayout(financial_group)

        self.subtotal_label = QLabel("0 تومان")
        self.discount_label = QLabel("0 تومان")
        self.total_label = QLabel("0 تومان")
        self.total_label.setStyleSheet("font-size:16px; font-weight:bold; color: green;")

        financial_layout.addRow("جمع جزء:", self.subtotal_label)
        financial_layout.addRow("تخفیف:", self.discount_label)
        financial_layout.addRow("مجموع نهایی:", self.total_label)

        layout.addWidget(financial_group)

        # کنترل‌های مدیریت سفارش
        controls_layout = QHBoxLayout()

        # دکمه‌های مدیریت آیتم
        self.remove_btn = QPushButton("❌ حذف آیتم انتخاب شده")
        self.remove_btn.clicked.connect(self.remove_selected_item)
        controls_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("🗑️ پاک کردن سفارش")
        self.clear_btn.clicked.connect(self.clear_order)
        controls_layout.addWidget(self.clear_btn)

        layout.addLayout(controls_layout)

        # بخش تخفیف
        discount_layout = QHBoxLayout()

        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("مبلغ تخفیف (تومان)")
        self.discount_input.setMaximumWidth(150)

        self.apply_discount_btn = QPushButton("✅ اعمال تخفیف")
        self.apply_discount_btn.clicked.connect(self.apply_discount)

        discount_layout.addWidget(QLabel("تخفیف:"))
        discount_layout.addWidget(self.discount_input)
        discount_layout.addWidget(self.apply_discount_btn)
        discount_layout.addStretch()

        layout.addLayout(discount_layout)

        # دکمه‌های نهایی
        final_layout = QHBoxLayout()

        self.print_test_btn = QPushButton("🖨️ تست پرینتر")
        self.print_test_btn.clicked.connect(self.print_test_receipt)
        final_layout.addWidget(self.print_test_btn)

        final_layout.addStretch()

        self.close_order_btn = QPushButton("💰 بستن سفارش")
        self.close_order_btn.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #4CAF50; color: white; padding: 10px;")
        self.close_order_btn.clicked.connect(self.close_order)
        final_layout.addWidget(self.close_order_btn)

        layout.addLayout(final_layout)

        # کی‌پد برای تست (بعداً حذف می‌شود)
        self.keypad = KeypadWidget()
        layout.addWidget(self.keypad)

        self.refresh_ui()

    def on_table_changed(self):
        """وقتی میز تغییر کرد"""
        table_text = self.table_combo.currentText()
        if table_text == "بیرون بر":
            table_number = None
        else:
            table_number = int(table_text.split()[1])  # استخراج عدد از "میز X"

        try:
            self.order_service.set_table(table_number)
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def refresh_ui(self):
        """به‌روزرسانی رابط کاربری"""
        self.order_list.clear()

        for item in self.order_service.get_items():
            # ایجاد ویجت سفارشی برای هر آیتم
            item_widget = OrderItemWidget(item.name, item.quantity, item.total_price().amount)
            item_widget.btn_remove.clicked.connect(lambda _, name=item.name: self.remove_item_by_name(name))
            item_widget.quantity_changed.connect(self.on_item_quantity_changed)

            # ایجاد QListWidgetItem و تنظیم ویجت سفارشی
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.order_list.addItem(list_item)
            self.order_list.setItemWidget(list_item, item_widget)

        # به‌روزرسانی برچسب‌های مالی
        subtotal = self.order_service.get_subtotal()
        discount = self.order_service.get_discount()
        total = self.order_service.get_total_price()

        self.subtotal_label.setText(str(subtotal))
        self.discount_label.setText(str(discount))
        self.total_label.setText(str(total))

    def remove_selected_item(self):
        """حذف آیتم انتخاب شده"""
        current_item = self.order_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "خطا", "لطفاً یک آیتم را انتخاب کنید")
            return

        # گرفتن ویجت آیتم انتخاب شده
        item_widget = self.order_list.itemWidget(current_item)
        if item_widget:
            item_name = item_widget.lbl_name.text()
            self.remove_item_by_name(item_name)

    def remove_item_by_name(self, name: str):
        """حذف آیتم بر اساس نام"""
        try:
            self.order_service.remove_item(name)
            self.refresh_ui()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def on_item_quantity_changed(self, name: str, new_quantity: int):
        """وقتی تعداد آیتم تغییر کرد"""
        try:
            self.order_service.change_quantity(name, new_quantity)
            self.refresh_ui()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def clear_order(self):
        """پاک کردن سفارش"""
        reply = QMessageBox.question(
            self, "تأیید",
            "آیا مطمئن هستید که می‌خواهید سفارش را پاک کنید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.order_service.clear()
            self.refresh_ui()

    def apply_discount(self):
        """اعمال تخفیف"""
        try:
            discount_text = self.discount_input.text().strip()
            if not discount_text:
                QMessageBox.warning(self, "خطا", "لطفاً مبلغ تخفیف را وارد کنید")
                return

            discount_amount = int(discount_text.replace(",", "").replace(" ", ""))
            self.order_service.apply_discount(discount_amount)
            self.discount_input.clear()
            self.refresh_ui()

        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در اعمال تخفیف: {str(e)}")

    def close_order(self):
        """بستن سفارش و ذخیره"""
        try:
            if not self.order_service.get_items():
                QMessageBox.warning(self, "خطا", "سفارش خالی نمی‌تواند بسته شود")
                return

            reply = QMessageBox.question(
                self, "تأیید بستن سفارش",
                f"مجموع سفارش: {self.order_service.get_total_price()}\n\nآیا سفارش را می‌بندید؟",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                order_id = self.order_service.close_and_save()

                # چاپ فاکتور
                try:
                    receipt_text = self.order_service.print_receipt(order_id)
                    QMessageBox.information(
                        self, "سفارش بسته شد",
                        f"سفارش با شماره {order_id} با موفقیت بسته و ذخیره شد\n\nفاکتور چاپ شد"
                    )
                except Exception as e:
                    QMessageBox.warning(
                        self, "سفارش بسته شد",
                        f"سفارش با شماره {order_id} ذخیره شد اما خطا در چاپ فاکتور:\n{str(e)}"
                    )

                self.refresh_ui()

        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بستن سفارش: {str(e)}")

    def print_test_receipt(self):
        """چاپ فاکتور تست"""
        try:
            self.order_service.print_test_receipt()
            QMessageBox.information(self, "تست پرینتر", "فاکتور تست با موفقیت چاپ شد")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در تست پرینتر: {str(e)}")
