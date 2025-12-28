# main_window.py - Clean POS-style main window
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QFrame, QScrollArea, QTabWidget,
    QListWidget, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal

from application.order_service import OrderService
from application.menu_service import MenuService
from ui.styles import POSStyles, FontManager, POSTheme


class POSMainWindow(QMainWindow):
    """Clean POS-style main window for cafe ordering system"""

    def __init__(self):
        super().__init__()
        self.order_service = OrderService()
        self.menu_service = MenuService()

        self.setWindowTitle("🍽️ سیستم ثبت سفارش کافه")
        self.resize(1400, 900)
        self.setMinimumSize(1200, 700)

        # Apply clean styling
        self.setStyleSheet(POSStyles.get_main_style())
        self.setFont(FontManager.get_main_font())

        self.setup_ui()
        self.load_menu_data()

    def setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Left side - Products
        self.setup_products_section(main_layout)

        # Right side - Cart
        self.setup_cart_section(main_layout)

        # Initialize with default table
        self.on_table_changed()

    def setup_products_section(self, parent_layout):
        """Setup products section with categories"""
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)

        # Header with table selection
        header_widget = QWidget()
        header_widget.setProperty("class", "header")
        header_layout = QHBoxLayout(header_widget)

        title_label = QLabel("🍽️ منوی کافه")
        title_label.setProperty("class", "header-title")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Table selection
        table_layout = QVBoxLayout()
        table_layout.setSpacing(5)

        table_label = QLabel("میز:")
        table_label.setStyleSheet("color: white; font-weight: bold;")
        table_layout.addWidget(table_label)

        self.table_combo = QComboBox()
        self.table_combo.addItems([f"میز {i}" for i in range(1, 21)])
        self.table_combo.addItem("بیرون بر")
        self.table_combo.setCurrentIndex(0)  # Default to table 1
        self.table_combo.currentIndexChanged.connect(self.on_table_changed)
        self.table_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.9);
                color: #1E293B;
                border: none;
                border-radius: 6px;
                padding: 8px;
                min-width: 120px;
            }
        """)
        table_layout.addWidget(self.table_combo)

        header_layout.addLayout(table_layout)
        products_layout.addWidget(header_widget)

        # Category tabs
        self.category_tabs = QTabWidget()
        self.category_tabs.setProperty("class", "categories")
        products_layout.addWidget(self.category_tabs)

        parent_layout.addWidget(products_widget, 2)

    def setup_cart_section(self, parent_layout):
        """Setup cart/order section"""
        cart_widget = QWidget()
        cart_widget.setProperty("class", "cart-section")
        cart_layout = QVBoxLayout(cart_widget)

        # Cart header
        cart_header = QLabel("🛒 سفارش جاری")
        cart_header.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1E293B;
                padding: 10px;
                border-bottom: 2px solid #E2E8F0;
            }
        """)
        cart_layout.addWidget(cart_header)

        # Order items list
        self.order_list = QListWidget()
        self.order_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
        """)
        cart_layout.addWidget(self.order_list, 1)

        # Total section
        total_widget = QWidget()
        total_layout = QVBoxLayout(total_widget)

        self.subtotal_label = QLabel("جمع جزء: 0 تومان")
        self.subtotal_label.setStyleSheet("color: #64748B; font-size: 14px;")

        self.discount_label = QLabel("تخفیف: 0 تومان")
        self.discount_label.setStyleSheet("color: #D97706; font-size: 14px;")

        self.total_label = QLabel("مجموع: 0 تومان")
        self.total_label.setProperty("class", "total-price")

        total_layout.addWidget(self.subtotal_label)
        total_layout.addWidget(self.discount_label)
        total_layout.addWidget(self.total_label)

        cart_layout.addWidget(total_widget)

        # Action buttons
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(10)

        self.checkout_btn = QPushButton("💰 تسویه حساب")
        self.checkout_btn.setProperty("class", "action-btn")
        self.checkout_btn.clicked.connect(self.checkout_order)
        buttons_layout.addWidget(self.checkout_btn)

        self.clear_btn = QPushButton("🗑️ پاک کردن سفارش")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_order)
        buttons_layout.addWidget(self.clear_btn)

        cart_layout.addWidget(buttons_widget)

        parent_layout.addWidget(cart_widget, 1)

    def load_menu_data(self):
        """Load menu data and create category tabs"""
        categories = self.menu_service.get_categories()

        # Create "همه" tab first
        all_tab = QWidget()
        all_layout = QVBoxLayout(all_tab)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        products_container = QWidget()
        self.all_grid = QGridLayout(products_container)
        self.all_grid.setSpacing(12)

        self.load_products_for_category("همه", self.all_grid)
        scroll_area.setWidget(products_container)
        all_layout.addWidget(scroll_area)

        self.category_tabs.addTab(all_tab, "🍽️ همه")

        # Create category tabs
        for category in sorted(categories):
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            products_container = QWidget()
            grid = QGridLayout(products_container)
            grid.setSpacing(12)

            self.load_products_for_category(category, grid)
            scroll_area.setWidget(products_container)
            tab_layout.addWidget(scroll_area)

            self.category_tabs.addTab(tab, f"📂 {category}")

    def load_products_for_category(self, category, grid_layout):
        """Load products for a specific category"""
        if category == "همه":
            products = self.menu_service.get_active_products()
        else:
            products = self.menu_service.get_products_by_category(category)

        row, col = 0, 0
        max_cols = 3  # 3 products per row

        for product in products:
            product_btn = QPushButton(f"{product.name}\n💰 {product.price:,} تومان")
            product_btn.setProperty("class", "product-btn")
            product_btn.setMinimumHeight(100)
            product_btn.clicked.connect(lambda checked, pid=product.id: self.add_product_to_order(pid))

            grid_layout.addWidget(product_btn, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def on_table_changed(self):
        """Handle table selection change"""
        table_text = self.table_combo.currentText()
        if table_text == "بیرون بر":
            table_number = None
        else:
            table_number = int(table_text.split()[1])

        try:
            self.order_service.set_table(table_number)
            self.refresh_cart()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def add_product_to_order(self, product_id):
        """Add product to current order"""
        try:
            product = self.menu_service.get_product_by_id(product_id)
            self.order_service.add_item(product.name, product.price, 1)
            self.refresh_cart()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", f"لطفاً ابتدا میز را انتخاب کنید: {str(e)}")

    def refresh_cart(self):
        """Refresh the cart display"""
        self.order_list.clear()

        for item in self.order_service.get_items():
            # Create order item widget
            item_widget = QWidget()
            item_widget.setProperty("class", "order-item")
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(10, 8, 10, 8)

            # Product name
            name_label = QLabel(item.name)
            name_label.setStyleSheet("font-weight: bold; font-size: 13px;")
            item_layout.addWidget(name_label)

            # Quantity control
            qty_spin = QSpinBox()
            qty_spin.setMinimum(1)
            qty_spin.setMaximum(99)
            qty_spin.setValue(item.quantity)
            qty_spin.setMaximumWidth(60)
            qty_spin.valueChanged.connect(
                lambda value, name=item.name: self.update_item_quantity(name, value)
            )
            item_layout.addWidget(qty_spin)

            # Price
            price_label = QLabel(f"{item.total_price().amount:,} تومان")
            price_label.setProperty("class", "price")
            item_layout.addWidget(price_label)

            # Remove button
            remove_btn = QPushButton("✕")
            remove_btn.setProperty("class", "remove-btn")
            remove_btn.clicked.connect(lambda checked, name=item.name: self.remove_item(name))
            item_layout.addWidget(remove_btn)

            # Add to list
            from PySide6.QtWidgets import QListWidgetItem
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.order_list.addItem(list_item)
            self.order_list.setItemWidget(list_item, item_widget)

        # Update totals
        subtotal = self.order_service.get_subtotal()
        discount = self.order_service.get_discount()
        total = self.order_service.get_total_price()

        self.subtotal_label.setText(f"جمع جزء: {subtotal.amount:,} تومان")
        self.discount_label.setText(f"تخفیف: {discount.amount:,} تومان")
        self.total_label.setText(f"مجموع: {total.amount:,} تومان")

    def update_item_quantity(self, item_name, new_quantity):
        """Update item quantity"""
        try:
            self.order_service.change_quantity(item_name, new_quantity)
            self.refresh_cart()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def remove_item(self, item_name):
        """Remove item from order"""
        try:
            self.order_service.remove_item(item_name)
            self.refresh_cart()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def checkout_order(self):
        """Checkout current order"""
        if not self.order_service.get_items():
            QMessageBox.warning(self, "خطا", "سفارش خالی نمی‌تواند تسویه شود")
            return

        total = self.order_service.get_total_price()

        reply = QMessageBox.question(
            self, "تأیید تسویه",
            f"مجموع سفارش: {total.amount:,} تومان\n\nآیا سفارش را تسویه می‌کنید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                order_id = self.order_service.close_and_save()
                QMessageBox.information(
                    self, "سفارش ثبت شد",
                    f"سفارش با شماره {order_id} با موفقیت ثبت و تسویه شد!"
                )
                self.refresh_cart()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ثبت سفارش: {str(e)}")

    def clear_order(self):
        """Clear current order"""
        if self.order_service.get_items():
            reply = QMessageBox.question(
                self, "تأیید پاک کردن",
                "آیا مطمئن هستید که می‌خواهید سفارش را پاک کنید؟",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Create new order instance for current table
                current_table = self.order_service.get_table_number()
                self.order_service = OrderService()
                if current_table:
                    self.order_service.set_table(current_table)
                self.refresh_cart()