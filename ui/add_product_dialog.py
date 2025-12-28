# ui/add_product_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QSpinBox, QComboBox, QMessageBox
)
from application.menu_service import MenuService


class AddProductDialog(QDialog):
    """Dialog for adding new products"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_service = MenuService()

        self.setWindowTitle("افزودن محصول جدید")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # Title
        title = QLabel("افزودن محصول جدید")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Product name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("نام محصول:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("مثال: قهوه latte")
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        # Price
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("قیمت (تومان):"))
        self.price_input = QSpinBox()
        self.price_input.setMinimum(0)
        self.price_input.setMaximum(10000000)
        self.price_input.setSuffix(" تومان")
        price_layout.addWidget(self.price_input)
        form_layout.addLayout(price_layout)

        # Category
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("دسته‌بندی:"))
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        # Load existing categories
        categories = self.menu_service.get_categories()
        self.category_combo.addItems(categories)
        if categories:
            self.category_combo.setCurrentText(categories[0])
        category_layout.addWidget(self.category_combo)
        form_layout.addLayout(category_layout)

        layout.addLayout(form_layout)

        # Buttons
        buttons_layout = QHBoxLayout()

        cancel_btn = QPushButton("❌ انصراف")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        add_btn = QPushButton("✅ افزودن محصول")
        add_btn.clicked.connect(self.add_product)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        buttons_layout.addWidget(add_btn)

        layout.addLayout(buttons_layout)

    def add_product(self):
        """Add the product"""
        name = self.name_input.text().strip()
        price = self.price_input.value()
        category = self.category_combo.currentText().strip()

        if not name:
            QMessageBox.warning(self, "خطا", "لطفاً نام محصول را وارد کنید")
            return

        if price <= 0:
            QMessageBox.warning(self, "خطا", "قیمت باید بیشتر از صفر باشد")
            return

        if not category:
            QMessageBox.warning(self, "خطا", "لطفاً دسته‌بندی را انتخاب کنید")
            return

        try:
            product_id = self.menu_service.add_product(name, price, category)
            QMessageBox.information(self, "موفق", f"محصول '{name}' با موفقیت اضافه شد!")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در افزودن محصول: {str(e)}")
