# ui/advanced_settings_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QMessageBox, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QSpinBox,
    QFormLayout, QTextEdit, QCheckBox, QDateEdit
)
from PySide6.QtCore import Qt
from datetime import datetime
from application.menu_service import MenuService


class AdvancedSettingsDialog(QDialog):
    """Advanced settings dialog for menu, tables, and customer loyalty"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_service = MenuService()

        self.setWindowTitle("⚙️ تنظیمات پیشرفته")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        # Header
        header_label = QLabel("تنظیمات پیشرفته سیستم")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header_label)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create tabs
        self.setup_menu_tab()
        self.setup_tables_tab()
        self.setup_loyalty_tab()
        self.setup_general_tab()

        # Buttons
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton("💾 ذخیره تغییرات")
        save_btn.clicked.connect(self.save_changes)
        buttons_layout.addWidget(save_btn)

        cancel_btn = QPushButton("❌ انصراف")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        self.load_current_settings()

    def setup_menu_tab(self):
        """Setup menu management tab"""
        menu_tab = QWidget()
        layout = QVBoxLayout(menu_tab)

        # Menu items table
        menu_group = QGroupBox("مدیریت آیتم‌های منو")
        menu_layout = QVBoxLayout(menu_group)

        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(4)
        self.menu_table.setHorizontalHeaderLabels(["نام محصول", "قیمت", "دسته‌بندی", "وضعیت"])
        menu_layout.addWidget(self.menu_table)

        # Menu controls
        controls_layout = QHBoxLayout()

        add_btn = QPushButton("➕ افزودن محصول")
        add_btn.clicked.connect(self.add_menu_item)
        controls_layout.addWidget(add_btn)

        edit_btn = QPushButton("✏️ ویرایش")
        edit_btn.clicked.connect(self.edit_menu_item)
        controls_layout.addWidget(edit_btn)

        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.clicked.connect(self.delete_menu_item)
        controls_layout.addWidget(delete_btn)

        refresh_btn = QPushButton("🔄 بروزرسانی")
        refresh_btn.clicked.connect(self.load_menu_items)
        controls_layout.addWidget(refresh_btn)

        menu_layout.addLayout(controls_layout)
        layout.addWidget(menu_group)

        layout.addStretch()
        self.tabs.addTab(menu_tab, "🍽️ منو")

    def setup_tables_tab(self):
        """Setup tables management tab"""
        tables_tab = QWidget()
        layout = QVBoxLayout(tables_tab)

        # Tables settings
        tables_group = QGroupBox("تنظیمات میزها")
        tables_layout = QVBoxLayout(tables_group)

        # Number of tables
        tables_count_layout = QHBoxLayout()
        tables_count_layout.addWidget(QLabel("تعداد میزها:"))

        self.tables_count_spin = QSpinBox()
        self.tables_count_spin.setMinimum(1)
        self.tables_count_spin.setMaximum(50)
        self.tables_count_spin.setValue(20)
        tables_count_layout.addWidget(self.tables_count_spin)

        tables_count_layout.addStretch()
        tables_layout.addLayout(tables_count_layout)

        # Table names customization
        names_group = QGroupBox("نام‌گذاری میزها")
        names_layout = QVBoxLayout(names_group)

        names_layout.addWidget(QLabel("در نسخه‌های بعدی قابل تنظیم خواهد بود."))
        tables_layout.addWidget(names_group)

        layout.addWidget(tables_group)

        # Table status
        status_group = QGroupBox("وضعیت میزها")
        status_layout = QVBoxLayout(status_group)

        self.table_status_table = QTableWidget()
        self.table_status_table.setColumnCount(3)
        self.table_status_table.setHorizontalHeaderLabels(["میز", "وضعیت", "سفارش جاری"])
        status_layout.addWidget(self.table_status_table)

        refresh_status_btn = QPushButton("🔄 بروزرسانی وضعیت")
        refresh_status_btn.clicked.connect(self.load_table_status)
        status_layout.addWidget(refresh_status_btn)

        layout.addWidget(status_group)

        layout.addStretch()
        self.tabs.addTab(tables_tab, "🪑 میزها")

    def setup_loyalty_tab(self):
        """Setup customer loyalty program tab"""
        loyalty_tab = QWidget()
        layout = QVBoxLayout(loyalty_tab)

        # Loyalty program settings
        program_group = QGroupBox("باشگاه مشتریان")
        program_layout = QVBoxLayout(program_group)

        # Enable/disable loyalty
        self.loyalty_enabled = QCheckBox("فعال کردن باشگاه مشتریان")
        self.loyalty_enabled.setChecked(True)
        program_layout.addWidget(self.loyalty_enabled)

        # Points system
        points_group = QGroupBox("سیستم امتیازدهی")
        points_layout = QFormLayout(points_group)

        self.points_per_toman = QSpinBox()
        self.points_per_toman.setMinimum(1)
        self.points_per_toman.setMaximum(100)
        self.points_per_toman.setValue(10)
        points_layout.addRow("امتیاز به ازای هر تومان:", self.points_per_toman)

        self.points_value = QSpinBox()
        self.points_value.setMinimum(1)
        self.points_value.setMaximum(1000)
        self.points_value.setValue(100)
        points_layout.addRow("ارزش هر امتیاز (ریال):", self.points_value)

        program_layout.addWidget(points_group)

        # Benefits
        benefits_group = QGroupBox("مزایای مشتریان")
        benefits_layout = QVBoxLayout(benefits_group)

        self.discount_levels = QTextEdit()
        self.discount_levels.setPlainText(
            "سطح 1: 100 امتیاز = 5% تخفیف\n"
            "سطح 2: 250 امتیاز = 10% تخفیف\n"
            "سطح 3: 500 امتیاز = 15% تخفیف\n"
            "سطح VIP: 1000 امتیاز = 20% تخفیف"
        )
        self.discount_levels.setMaximumHeight(100)
        benefits_layout.addWidget(self.discount_levels)

        program_layout.addWidget(benefits_group)
        layout.addWidget(program_group)

        # Customer management
        customers_group = QGroupBox("مدیریت مشتریان")
        customers_layout = QVBoxLayout(customers_group)

        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(4)
        self.customers_table.setHorizontalHeaderLabels(["نام", "شماره تماس", "امتیاز", "سطح"])
        customers_layout.addWidget(self.customers_table)

        customer_controls = QHBoxLayout()

        add_customer_btn = QPushButton("👤 افزودن مشتری")
        add_customer_btn.clicked.connect(self.add_customer)
        customer_controls.addWidget(add_customer_btn)

        edit_customer_btn = QPushButton("✏️ ویرایش")
        edit_customer_btn.clicked.connect(self.edit_customer)
        customer_controls.addWidget(edit_customer_btn)

        customers_layout.addLayout(customer_controls)
        layout.addWidget(customers_group)

        layout.addStretch()
        self.tabs.addTab(loyalty_tab, "⭐ باشگاه مشتریان")

    def setup_general_tab(self):
        """Setup general settings tab"""
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)

        # Business info
        business_group = QGroupBox("اطلاعات کسب‌وکار")
        business_layout = QFormLayout(business_group)

        self.business_name = QLineEdit("کافه نمونه")
        business_layout.addRow("نام کافه:", self.business_name)

        self.business_address = QLineEdit("تهران، خیابان ولیعصر")
        business_layout.addRow("آدرس:", self.business_address)

        self.business_phone = QLineEdit("021-12345678")
        business_layout.addRow("تلفن:", self.business_phone)

        layout.addWidget(business_group)

        # Receipt settings
        receipt_group = QGroupBox("تنظیمات فاکتور")
        receipt_layout = QVBoxLayout(receipt_group)

        self.receipt_footer = QTextEdit()
        self.receipt_footer.setPlainText(
            "با تشکر از انتخاب شما!\n"
            "آدرس: تهران، خیابان ولیعصر\n"
            "تلفن: 021-12345678"
        )
        self.receipt_footer.setMaximumHeight(80)
        receipt_layout.addWidget(QLabel("متن پاورقی فاکتور:"))
        receipt_layout.addWidget(self.receipt_footer)

        layout.addWidget(receipt_group)

        # System settings
        system_group = QGroupBox("تنظیمات سیستم")
        system_layout = QVBoxLayout(system_group)

        self.auto_backup = QCheckBox("پشتیبان‌گیری خودکار روزانه")
        self.auto_backup.setChecked(True)
        system_layout.addWidget(self.auto_backup)

        self.confirm_delete = QCheckBox("تأیید حذف آیتم‌ها")
        self.confirm_delete.setChecked(True)
        system_layout.addWidget(self.confirm_delete)

        layout.addWidget(system_group)

        layout.addStretch()
        self.tabs.addTab(general_tab, "🔧 عمومی")

    def load_current_settings(self):
        """Load current settings"""
        self.load_menu_items()
        self.load_table_status()
        self.load_customers()

    def load_menu_items(self):
        """Load menu items into table"""
        products = self.menu_service.get_active_products()

        self.menu_table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.menu_table.setItem(row, 0, QTableWidgetItem(product.name))
            self.menu_table.setItem(row, 1, QTableWidgetItem(f"{product.price:,}"))
            self.menu_table.setItem(row, 2, QTableWidgetItem(product.category))
            self.menu_table.setItem(row, 3, QTableWidgetItem("فعال" if product.is_active else "غیرفعال"))

        self.menu_table.resizeColumnsToContents()

    def load_table_status(self):
        """Load table status"""
        # For now, just show table numbers
        tables_count = self.tables_count_spin.value()
        self.table_status_table.setRowCount(tables_count)

        for i in range(tables_count):
            self.table_status_table.setItem(i, 0, QTableWidgetItem(f"میز {i+1}"))
            self.table_status_table.setItem(i, 1, QTableWidgetItem("خالی"))
            self.table_status_table.setItem(i, 2, QTableWidgetItem("-"))

        self.table_status_table.resizeColumnsToContents()

    def load_customers(self):
        """Load customer data"""
        # Sample data for now
        sample_customers = [
            ["احمد رضایی", "09123456789", "150", "سطح 1"],
            ["مریم احمدی", "09198765432", "450", "سطح 2"],
            ["علی محمدی", "09155556666", "850", "سطح VIP"]
        ]

        self.customers_table.setRowCount(len(sample_customers))
        for row, customer in enumerate(sample_customers):
            for col, data in enumerate(customer):
                self.customers_table.setItem(row, col, QTableWidgetItem(data))

        self.customers_table.resizeColumnsToContents()

    def add_menu_item(self):
        """Add new menu item"""
        from ui.add_product_dialog import AddProductDialog
        dialog = AddProductDialog(self)
        if dialog.exec():
            self.load_menu_items()
            QMessageBox.information(self, "موفق", "محصول جدید اضافه شد!")

    def edit_menu_item(self):
        """Edit selected menu item"""
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک محصول را انتخاب کنید")
            return

        product_name = self.menu_table.item(current_row, 0).text()
        QMessageBox.information(self, "توجه", f"ویرایش محصول '{product_name}' در نسخه‌های بعدی اضافه خواهد شد.")

    def delete_menu_item(self):
        """Delete selected menu item"""
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک محصول را انتخاب کنید")
            return

        product_name = self.menu_table.item(current_row, 0).text()

        if self.confirm_delete.isChecked():
            reply = QMessageBox.question(
                self, "تأیید حذف",
                f"آیا مطمئن هستید که محصول '{product_name}' را حذف کنید؟",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        # Here you would actually delete the product
        QMessageBox.information(self, "موفق", f"محصول '{product_name}' حذف شد!")

    def add_customer(self):
        """Add new customer"""
        from ui.add_customer_dialog import AddCustomerDialog
        dialog = AddCustomerDialog(self)
        if dialog.exec():
            self.load_customers()
            QMessageBox.information(self, "موفق", "مشتری جدید اضافه شد!")

    def edit_customer(self):
        """Edit selected customer"""
        current_row = self.customers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "لطفاً یک مشتری را انتخاب کنید")
            return

        customer_name = self.customers_table.item(current_row, 0).text()
        QMessageBox.information(self, "توجه", f"ویرایش مشتری '{customer_name}' در نسخه‌های بعدی اضافه خواهد شد.")

    def save_changes(self):
        """Save all changes"""
        # Here you would save all settings to database/file
        QMessageBox.information(self, "موفق", "تنظیمات ذخیره شد!")
        self.accept()
