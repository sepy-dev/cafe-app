# main_window.py - Clean POS-style main window
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QFrame, QScrollArea, QTabWidget,
    QListWidget, QSpinBox, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt, Signal, QTimer
from datetime import datetime

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
        self.setup_timers()
        self.setup_shortcuts()

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

    def setup_quick_actions(self, parent_layout):
        """Setup quick action buttons"""
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 5, 0, 10)
        actions_layout.setSpacing(8)

        # Popular items button
        popular_btn = QPushButton("⭐ محبوب‌ترین")
        popular_btn.clicked.connect(self.show_popular_items)
        popular_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)
        actions_layout.addWidget(popular_btn)

        # Recent orders button
        recent_btn = QPushButton("🕐 اخیر")
        recent_btn.clicked.connect(self.show_recent_orders)
        recent_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        actions_layout.addWidget(recent_btn)

        # Customer info button
        customer_btn = QPushButton("👤 مشتری")
        customer_btn.clicked.connect(self.show_customer_info)
        customer_btn.setStyleSheet("""
            QPushButton {
                background-color: #06B6D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0891B2;
            }
        """)
        actions_layout.addWidget(customer_btn)

        actions_layout.addStretch()

        # Keyboard shortcuts hint
        shortcuts_label = QLabel("⌨️ F12: تسویه • Ctrl+F: جستجو • F1-F9: میزها")
        shortcuts_label.setStyleSheet("font-size: 10px; color: #64748B;")
        actions_layout.addWidget(shortcuts_label)

        parent_layout.addWidget(actions_widget)

    def setup_timers(self):
        """Setup timers for real-time updates"""
        # Time update timer
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Update every second

        # Stats update timer
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(5000)  # Update every 5 seconds

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        from PySide6.QtGui import QShortcut, QKeySequence

        # Checkout shortcut (F12)
        checkout_shortcut = QShortcut(QKeySequence("F12"), self)
        checkout_shortcut.activated.connect(self.checkout_order)

        # Clear order shortcut (Ctrl+Del)
        clear_shortcut = QShortcut(QKeySequence("Ctrl+Delete"), self)
        clear_shortcut.activated.connect(self.clear_order)

        # Focus search shortcut (Ctrl+F)
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(lambda: self.search_input.setFocus())

        # New order shortcut (Ctrl+N)
        new_order_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_order_shortcut.activated.connect(self.clear_order)

        # Print shortcut (Ctrl+P)
        print_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        print_shortcut.activated.connect(self.print_current_receipt)

        # Table shortcuts (F1-F9 for tables 1-9)
        for i in range(1, 10):
            table_shortcut = QShortcut(QKeySequence(f"F{i}"), self)
            table_shortcut.activated.connect(lambda table=i: self.quick_table_select(table))

    def setup_products_section(self, parent_layout):
        """Setup products section with categories"""
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)

        # Enhanced Header with multiple controls
        header_widget = QWidget()
        header_widget.setProperty("class", "header")
        header_widget.setFixedHeight(80)  # Fixed height for better appearance
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)

        # Left side - Title and branding
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title_label = QLabel("🍽️ سیستم ثبت سفارش کافه")
        title_label.setProperty("class", "header-title")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("ساده، سریع و حرفه‌ای")
        subtitle_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.8);")
        title_layout.addWidget(subtitle_label)

        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        # Center - Current table indicator
        table_indicator_layout = QVBoxLayout()
        table_indicator_layout.setSpacing(2)
        table_indicator_layout.setAlignment(Qt.AlignCenter)

        table_indicator_title = QLabel("میز فعلی")
        table_indicator_title.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold;")
        table_indicator_layout.addWidget(table_indicator_title)

        self.table_indicator = QLabel("میز ۱")
        self.table_indicator.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FFD700;
                background-color: rgba(255,255,255,0.1);
                padding: 8px 16px;
                border-radius: 20px;
                border: 2px solid rgba(255,255,255,0.3);
            }
        """)
        table_indicator_layout.addWidget(self.table_indicator)

        header_layout.addLayout(table_indicator_layout)

        header_layout.addStretch()

        # Right side - Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        # Theme selector
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(2)

        theme_label = QLabel("تم")
        theme_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold;")
        theme_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["🔵 آبی مدرن", "🌙 تاریک", "🟠 گرم نارنجی"])
        self.theme_combo.setCurrentIndex(0)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.9);
                color: #1E293B;
                border: none;
                border-radius: 6px;
                padding: 6px;
                min-width: 120px;
                font-size: 11px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)
        theme_layout.addWidget(self.theme_combo)
        controls_layout.addLayout(theme_layout)

        # Table selector
        table_select_layout = QVBoxLayout()
        table_select_layout.setSpacing(2)

        table_select_label = QLabel("تغییر میز")
        table_select_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold;")
        table_select_layout.addWidget(table_select_label)

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
                padding: 6px;
                min-width: 100px;
                font-size: 11px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)
        table_select_layout.addWidget(self.table_combo)
        controls_layout.addLayout(table_select_layout)

        # Settings button
        settings_btn = QPushButton("⚙️")
        settings_btn.setToolTip("تنظیمات پیشرفته")
        settings_btn.clicked.connect(self.show_settings)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.1);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
                border-color: rgba(255,255,255,0.5);
            }
        """)
        controls_layout.addWidget(settings_btn)

        header_layout.addLayout(controls_layout)
        products_layout.addWidget(header_widget)

        # Search bar
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 10)

        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 16px; color: #64748B;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو محصولات...")
        self.search_input.textChanged.connect(self.filter_products)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2563EB;
            }
        """)

        clear_search_btn = QPushButton("❌")
        clear_search_btn.setToolTip("پاک کردن جستجو")
        clear_search_btn.clicked.connect(lambda: self.search_input.clear())
        clear_search_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #94A3B8;
                padding: 8px;
            }
            QPushButton:hover {
                color: #DC2626;
            }
        """)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(clear_search_btn)
        products_layout.addLayout(search_layout)

        # Category tabs with improved styling
        self.category_tabs = QTabWidget()
        self.category_tabs.setProperty("class", "categories")
        self.category_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background-color: #F1F5F9;
                color: #64748B;
                border: none;
                padding: 12px 20px;
                margin-right: 2px;
                border-radius: 8px 8px 0 0;
                font-size: 13px;
                font-weight: 500;
                min-width: 90px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #2563EB;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #E2E8F0;
                color: #475569;
            }
        """)
        products_layout.addWidget(self.category_tabs)

        # Quick action bar
        self.setup_quick_actions(products_layout)

        parent_layout.addWidget(products_widget, 2)

    def setup_cart_section(self, parent_layout):
        """Setup enhanced cart/order section"""
        cart_widget = QWidget()
        cart_widget.setProperty("class", "cart-section")
        cart_layout = QVBoxLayout(cart_widget)

        # Enhanced Cart header with time and stats
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Title and time
        title_time_layout = QHBoxLayout()
        cart_title = QLabel("🛒 سفارش جاری")
        cart_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B;")

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 12px; color: #64748B;")
        self.update_time()

        title_time_layout.addWidget(cart_title)
        title_time_layout.addStretch()
        title_time_layout.addWidget(self.time_label)
        header_layout.addLayout(title_time_layout)

        # Quick stats
        self.stats_label = QLabel("📊 ۰ سفارش • ۰ تومان")
        self.stats_label.setStyleSheet("font-size: 11px; color: #64748B; margin-top: 2px;")
        header_layout.addWidget(self.stats_label)

        cart_layout.addWidget(header_widget)

        # Order items list with improved styling
        self.order_list = QListWidget()
        self.order_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                background-color: #FAFAFA;
                padding: 5px;
            }
            QListWidget::item {
                border-bottom: 1px solid #F1F5F9;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #F1F5F9;
            }
        """)
        cart_layout.addWidget(self.order_list, 1)

        # Discount input section
        discount_widget = QWidget()
        discount_layout = QHBoxLayout(discount_widget)
        discount_layout.setContentsMargins(10, 5, 10, 5)

        discount_label = QLabel("تخفیف:")
        discount_label.setStyleSheet("font-size: 12px; color: #64748B;")

        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("مبلغ تخفیف")
        self.discount_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 12px;
                max-width: 80px;
            }
            QLineEdit:focus {
                border-color: #F59E0B;
            }
        """)

        apply_discount_btn = QPushButton("✅ اعمال")
        apply_discount_btn.clicked.connect(self.apply_discount)
        apply_discount_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)

        discount_layout.addWidget(discount_label)
        discount_layout.addWidget(self.discount_input)
        discount_layout.addWidget(apply_discount_btn)
        discount_layout.addStretch()

        cart_layout.addWidget(discount_widget)

        # Total section with better styling
        total_widget = QWidget()
        total_widget.setStyleSheet("""
            QWidget {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                margin: 5px;
            }
        """)
        total_layout = QVBoxLayout(total_widget)
        total_layout.setContentsMargins(15, 10, 15, 10)

        self.subtotal_label = QLabel("جمع جزء: 0 تومان")
        self.subtotal_label.setStyleSheet("color: #64748B; font-size: 13px;")

        self.discount_label = QLabel("تخفیف: 0 تومان")
        self.discount_label.setStyleSheet("color: #D97706; font-size: 13px;")

        # Separator line
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #E2E8F0;")
        total_layout.addWidget(separator)

        self.total_label = QLabel("مجموع: 0 تومان")
        self.total_label.setProperty("class", "total-price")
        self.total_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #059669;
                margin-top: 5px;
            }
        """)

        total_layout.addWidget(self.subtotal_label)
        total_layout.addWidget(self.discount_label)
        total_layout.addWidget(separator)
        total_layout.addWidget(self.total_label)

        cart_layout.addWidget(total_widget)

        # Action buttons with improved layout
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(8)
        buttons_layout.setContentsMargins(10, 5, 10, 10)

        self.checkout_btn = QPushButton("💰 تسویه حساب")
        self.checkout_btn.setProperty("class", "action-btn")
        self.checkout_btn.clicked.connect(self.checkout_order)
        buttons_layout.addWidget(self.checkout_btn)

        # Additional buttons
        extra_buttons_layout = QHBoxLayout()
        extra_buttons_layout.setSpacing(8)

        self.print_receipt_btn = QPushButton("🖨️ چاپ قبض")
        self.print_receipt_btn.clicked.connect(self.print_current_receipt)
        self.print_receipt_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        extra_buttons_layout.addWidget(self.print_receipt_btn)

        self.clear_btn = QPushButton("🗑️ پاک کردن")
        self.clear_btn.clicked.connect(self.clear_order)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        extra_buttons_layout.addWidget(self.clear_btn)

        buttons_layout.addLayout(extra_buttons_layout)
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
            # Create product card widget
            product_card = self.create_product_card(product)
            grid_layout.addWidget(product_card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def on_table_changed(self):
        """Handle table selection change"""
        table_text = self.table_combo.currentText()
        if table_text == "بیرون بر":
            table_number = None
            display_text = "بیرون بر"
        else:
            table_number = int(table_text.split()[1])
            display_text = f"میز {table_number}"

        try:
            self.order_service.set_table(table_number)
            self.table_indicator.setText(display_text)

            # Update indicator color based on table type
            if table_number is None:
                self.table_indicator.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #FFA500;
                        background-color: rgba(255,165,0,0.1);
                        padding: 8px 16px;
                        border-radius: 20px;
                        border: 2px solid rgba(255,165,0,0.3);
                    }
                """)
            else:
                self.table_indicator.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #FFD700;
                        background-color: rgba(255,255,255,0.1);
                        padding: 8px 16px;
                        border-radius: 20px;
                        border: 2px solid rgba(255,255,255,0.3);
                    }
                """)

            self.refresh_cart()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def add_product_to_order(self, product_id):
        """Add product to current order"""
        try:
            product = self.menu_service.get_product_by_id(product_id)
            self.order_service.add_item(product.name, product.price, 1)
            self.refresh_cart()
            self.show_notification("محصول اضافه شد", f"{product.name} به سفارش اضافه شد", "✅")
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
                total_amount = total.amount
                QMessageBox.information(
                    self, "سفارش ثبت شد",
                    f"سفارش با شماره {order_id} با موفقیت ثبت و تسویه شد!\n\nمجموع: {total_amount:,} تومان"
                )
                self.show_notification("سفارش تسویه شد", f"مبلغ: {total_amount:,} تومان", "💰")
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

    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y/%m/%d")
        self.time_label.setText(f"📅 {current_date} 🕐 {current_time}")

    def update_stats(self):
        """Update daily statistics display"""
        try:
            from application.report_service import ReportService
            report_service = ReportService()
            today_stats = report_service.get_daily_sales()

            order_count = today_stats['orders_count']
            total_sales = today_stats['net_sales'].amount

            self.stats_label.setText(f"📊 {order_count} سفارش • {total_sales:,} تومان")
        except:
            # If stats fail, just update with current order info
            items_count = len(self.order_service.get_items())
            self.stats_label.setText(f"📊 {items_count} آیتم")

    def apply_discount(self):
        """Apply discount to current order"""
        try:
            discount_text = self.discount_input.text().strip()
            if not discount_text:
                QMessageBox.warning(self, "خطا", "لطفاً مبلغ تخفیف را وارد کنید")
                return

            discount_amount = int(discount_text.replace(",", "").replace(" ", ""))
            self.order_service.apply_discount(discount_amount)
            self.discount_input.clear()
            self.refresh_cart()
            QMessageBox.information(self, "موفق", f"تخفیف {discount_amount:,} تومان اعمال شد!")
        except ValueError as e:
            QMessageBox.warning(self, "خطا", f"مبلغ تخفیف نامعتبر: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در اعمال تخفیف: {str(e)}")

    def print_current_receipt(self):
        """Print receipt for current order"""
        if not self.order_service.get_items():
            QMessageBox.warning(self, "خطا", "سفارش خالی نمی‌تواند چاپ شود")
            return

        try:
            from infrastructure.printer.receipt_printer import ReceiptPrinter
            printer = ReceiptPrinter()

            # Create a temporary order with current items for printing
            temp_order = type('TempOrder', (), {})()
            temp_order.items = self.order_service.get_items()
            temp_order.status = type('Status', (), {'value': 'CLOSED'})()
            temp_order.discount = self.order_service.get_discount()
            temp_order.total_price = lambda: self.order_service.get_total_price()
            temp_order.table_number = self.order_service.get_table_number()

            receipt_text = printer.print_receipt(temp_order, 0)
            QMessageBox.information(self, "موفق", "فاکتور به پرینتر ارسال شد!")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در چاپ فاکتور: {str(e)}")

    def quick_table_select(self, table_number):
        """Quick table selection via keyboard shortcuts"""
        if 1 <= table_number <= 20:
            self.table_combo.setCurrentIndex(table_number - 1)  # 0-based index

    def show_popular_items(self):
        """Show popular items tab"""
        # Switch to first tab (All items)
        self.category_tabs.setCurrentIndex(0)
        self.show_notification("محبوب‌ترین محصولات", "تب همه محصولات نمایش داده شد", "⭐")

    def show_recent_orders(self):
        """Show recent orders dialog"""
        try:
            from application.report_service import ReportService
            report_service = ReportService()

            # Get today's orders
            today_report = report_service.get_daily_sales()
            popular_products = today_report.get('top_products', [])

            if popular_products:
                message = "محبوب‌ترین محصولات امروز:\n" + "\n".join([
                    f"• {p['name']}: {p['quantity']} عدد"
                    for p in popular_products[:5]
                ])
            else:
                message = "هنوز سفارشی ثبت نشده است"

            QMessageBox.information(self, "سفارشات اخیر", message)
        except Exception as e:
            QMessageBox.information(self, "سفارشات اخیر", "امکان نمایش آمار وجود ندارد")

    def show_customer_info(self):
        """Show customer information dialog"""
        current_table = self.order_service.get_table_number()
        items_count = len(self.order_service.get_items())
        total_amount = self.order_service.get_total_price().amount

        info_text = f"""
        📊 اطلاعات سفارش جاری:

        میز: {"بیرون بر" if current_table is None else f"میز {current_table}"}
        تعداد آیتم‌ها: {items_count}
        مجموع مبلغ: {total_amount:,} تومان
        زمان: {datetime.now().strftime("%H:%M:%S")}
        """

        QMessageBox.information(self, "اطلاعات مشتری", info_text.strip())

    def show_notification(self, title, message, icon="ℹ️"):
        """Show a notification toast"""
        # Create notification widget
        notification = QWidget(self)
        notification.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        notification.setStyleSheet("""
            QWidget {
                background-color: #1F2937;
                color: white;
                border-radius: 8px;
                padding: 12px;
                border: 1px solid #374151;
            }
        """)

        layout = QHBoxLayout(notification)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px; margin-right: 8px;")

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        message_label = QLabel(message)
        message_label.setStyleSheet("font-size: 11px; color: #D1D5DB;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)

        layout.addWidget(icon_label)
        layout.addLayout(text_layout)

        # Position and show
        notification.adjustSize()
        notification.move(self.width() - notification.width() - 20,
                         self.height() - notification.height() - 20)
        notification.show()

        # Auto hide after 3 seconds
        QTimer.singleShot(3000, notification.hide)

    def create_product_card(self, product):
        """Create an enhanced product card"""
        card = QWidget()
        card.setFixedSize(160, 140)  # Fixed size for consistent layout
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #E2E8F0;
                border-radius: 12px;
                margin: 4px;
            }
            QWidget:hover {
                border-color: #2563EB;
                background-color: #F8FAFC;
                transform: translateY(-2px);
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Product name
        name_label = QLabel(product.name[:15] + "..." if len(product.name) > 15 else product.name)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #1E293B;
                text-align: center;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # Category badge
        category_label = QLabel(f"📂 {product.category[:8]}..." if len(product.category) > 8 else f"📂 {product.category}")
        category_label.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #64748B;
                background-color: #F1F5F9;
                padding: 2px 4px;
                border-radius: 6px;
                text-align: center;
            }
        """)
        category_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(category_label)

        # Price
        price_label = QLabel(f"💰 {product.price:,}")
        price_label.setProperty("class", "price")
        price_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #F59E0B;
                text-align: center;
                margin-top: 2px;
            }
        """)
        price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(price_label)

        # Add to cart button
        add_btn = QPushButton("➕")
        add_btn.setToolTip(f"افزودن {product.name} به سفارش")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_product_to_order(product.id))
        layout.addWidget(add_btn)

        return card

    def filter_products(self):
        """Filter products based on search text"""
        search_text = self.search_input.text().lower().strip()

        # Hide/show products based on search
        for tab_index in range(self.category_tabs.count()):
            tab_widget = self.category_tabs.widget(tab_index)
            if tab_widget and hasattr(tab_widget, 'layout'):
                layout = tab_widget.layout()
                if layout:
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if item and item.widget():
                            widget = item.widget()
                            if hasattr(widget, 'findChildren'):
                                # Find labels in the card
                                labels = widget.findChildren(QLabel)
                                visible = not search_text  # Show all if no search

                                for label in labels:
                                    if search_text in label.text().lower():
                                        visible = True
                                        break

                                widget.setVisible(visible)

    def change_theme(self):
        """Change application theme"""
        theme_index = self.theme_combo.currentIndex()

        if theme_index == 0:  # Modern Blue
            self.apply_theme("modern_blue")
        elif theme_index == 1:  # Dark
            self.apply_theme("dark")
        elif theme_index == 2:  # Warm Orange
            self.apply_theme("warm_orange")

        QMessageBox.information(self, "تم تغییر یافت", f"تم به '{self.theme_combo.currentText()}' تغییر یافت!")

    def apply_theme(self, theme_name):
        """Apply a specific theme"""
        from ui.styles import POSTheme

        if theme_name == "modern_blue":
            POSTheme.PRIMARY = "#2563EB"
            POSTheme.SECONDARY = "#10B981"
            POSTheme.ACCENT = "#F59E0B"
        elif theme_name == "dark":
            POSTheme.PRIMARY = "#6366F1"
            POSTheme.SECONDARY = "#8B5CF6"
            POSTheme.ACCENT = "#F59E0B"
            POSTheme.BG_MAIN = "#1F2937"
            POSTheme.BG_SECONDARY = "#111827"
            POSTheme.TEXT_PRIMARY = "#F9FAFB"
            POSTheme.TEXT_SECONDARY = "#D1D5DB"
        elif theme_name == "warm_orange":
            POSTheme.PRIMARY = "#EA580C"
            POSTheme.SECONDARY = "#059669"
            POSTheme.ACCENT = "#DC2626"
            POSTheme.BG_SECONDARY = "#FFF7ED"

        # Reapply styles
        self.setStyleSheet(POSStyles.get_main_style())

    def show_settings(self):
        """Show advanced settings dialog"""
        from ui.printer_settings_dialog import PrinterSettingsDialog
        dialog = PrinterSettingsDialog(self)
        dialog.exec()