# menu_management_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QFormLayout, QSpinBox, QGroupBox
)
from PySide6.QtCore import Qt
from application.menu_service import MenuService


class MenuManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_service = MenuService()
        self.current_product_id = None

        self.setWindowTitle("مدیریت منو")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # عنوان
        title = QLabel("مدیریت محصولات منو")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # جدول محصولات
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "نام", "قیمت", "دسته‌بندی", "وضعیت"])
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.itemSelectionChanged.connect(self.on_product_selected)
        layout.addWidget(self.products_table)

        # دکمه‌های مدیریت
        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ افزودن محصول")
        self.add_btn.clicked.connect(self.show_add_form)
        buttons_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("✏️ ویرایش")
        self.edit_btn.clicked.connect(self.show_edit_form)
        self.edit_btn.setEnabled(False)
        buttons_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑️ حذف")
        self.delete_btn.clicked.connect(self.delete_product)
        self.delete_btn.setEnabled(False)
        buttons_layout.addWidget(self.delete_btn)

        self.refresh_btn = QPushButton("🔄 بروزرسانی")
        self.refresh_btn.clicked.connect(self.load_products)
        buttons_layout.addWidget(self.refresh_btn)

        layout.addLayout(buttons_layout)

        # فرم افزودن/ویرایش محصول
        self.form_group = QGroupBox("افزودن/ویرایش محصول")
        self.form_group.setVisible(False)
        form_layout = QFormLayout(self.form_group)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("نام محصول")
        form_layout.addRow("نام محصول:", self.name_input)

        self.price_input = QSpinBox()
        self.price_input.setMinimum(0)
        self.price_input.setMaximum(10000000)
        self.price_input.setSuffix(" تومان")
        form_layout.addRow("قیمت:", self.price_input)

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(self.menu_service.get_categories())
        form_layout.addRow("دسته‌بندی:", self.category_input)

        form_buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("💾 ذخیره")
        self.save_btn.clicked.connect(self.save_product)
        form_buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("❌ انصراف")
        self.cancel_btn.clicked.connect(self.hide_form)
        form_buttons_layout.addWidget(self.cancel_btn)

        form_layout.addRow(form_buttons_layout)

        layout.addWidget(self.form_group)

        self.load_products()

    def load_products(self):
        """بارگذاری محصولات در جدول"""
        products = self.menu_service.get_active_products()

        self.products_table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.products_table.setItem(row, 2, QTableWidgetItem(f"{product.price:,} تومان"))
            self.products_table.setItem(row, 3, QTableWidgetItem(product.category))
            status = "فعال" if product.is_active else "غیرفعال"
            self.products_table.setItem(row, 4, QTableWidgetItem(status))

        self.products_table.resizeColumnsToContents()

    def on_product_selected(self):
        """وقتی محصولی انتخاب شد"""
        selected_rows = set()
        for item in self.products_table.selectedItems():
            selected_rows.add(item.row())

        has_selection = len(selected_rows) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def show_add_form(self):
        """نمایش فرم افزودن محصول"""
        self.current_product_id = None
        self.form_group.setTitle("افزودن محصول جدید")
        self.name_input.clear()
        self.price_input.setValue(0)
        self.category_input.setCurrentText("")
        self.save_btn.setText("➕ افزودن")
        self.form_group.setVisible(True)

    def show_edit_form(self):
        """نمایش فرم ویرایش محصول"""
        selected_items = self.products_table.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        product_id = int(self.products_table.item(row, 0).text())

        try:
            product = self.menu_service.get_product_by_id(product_id)

            self.current_product_id = product.id
            self.form_group.setTitle("ویرایش محصول")
            self.name_input.setText(product.name)
            self.price_input.setValue(product.price)
            self.category_input.setCurrentText(product.category)
            self.save_btn.setText("💾 بروزرسانی")
            self.form_group.setVisible(True)

        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def hide_form(self):
        """پنهان کردن فرم"""
        self.form_group.setVisible(False)
        self.current_product_id = None

    def save_product(self):
        """ذخیره محصول"""
        name = self.name_input.text().strip()
        price = self.price_input.value()
        category = self.category_input.currentText().strip()

        if not name:
            QMessageBox.warning(self, "خطا", "نام محصول را وارد کنید")
            return

        if price <= 0:
            QMessageBox.warning(self, "خطا", "قیمت باید مثبت باشد")
            return

        if not category:
            QMessageBox.warning(self, "خطا", "دسته‌بندی را انتخاب کنید")
            return

        try:
            if self.current_product_id:
                # ویرایش محصول موجود
                self.menu_service.update_product(
                    product_id=self.current_product_id,
                    name=name,
                    price=price,
                    category=category
                )
                QMessageBox.information(self, "موفق", "محصول با موفقیت بروزرسانی شد")
            else:
                # افزودن محصول جدید
                product_id = self.menu_service.add_product(name, price, category)
                QMessageBox.information(self, "موفق", f"محصول جدید با ID {product_id} اضافه شد")

            self.hide_form()
            self.load_products()

        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def delete_product(self):
        """حذف محصول"""
        selected_items = self.products_table.selectedItems()
        if not selected_items:
            return

        row = selected_items[0].row()
        product_id = int(self.products_table.item(row, 0).text())
        product_name = self.products_table.item(row, 1).text()

        reply = QMessageBox.question(
            self, "تأیید حذف",
            f"آیا مطمئن هستید که می‌خواهید محصول '{product_name}' را حذف کنید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.menu_service.delete_product(product_id)
                QMessageBox.information(self, "موفق", "محصول با موفقیت حذف شد")
                self.load_products()
            except ValueError as e:
                QMessageBox.warning(self, "خطا", str(e))
