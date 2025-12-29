# ui/advanced_settings_dialog.py - Modern Settings Dialog
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QMessageBox, QTabWidget, QWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QSpinBox,
    QFormLayout, QTextEdit, QCheckBox, QHeaderView, QScrollArea,
    QFrame, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from application.menu_service import MenuService
from ui.styles import ThemeManager


class AdvancedSettingsDialog(QDialog):
    """Modern advanced settings dialog with full menu and table management"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_service = MenuService()
        self.theme_manager = ThemeManager()
        self.theme = self.theme_manager.current_theme
        
        # State
        self.tables_count = 20
        self.table_orders = {}  # {table_num: order_count}

        self.setWindowTitle("⚙️ تنظیمات پیشرفته")
        self.resize(900, 700)
        self.setMinimumSize(700, 500)
        
        self.apply_styles()
        self.setup_ui()
        self.load_current_settings()

    def apply_styles(self):
        """Apply theme styles to dialog"""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.theme.get('bg_main')};
                color: {self.theme.get('text_primary')};
            }}
            QLabel {{
                color: {self.theme.get('text_primary')};
            }}
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 1px solid {self.theme.get('border_light')};
                border-radius: 12px;
                margin-top: 20px;
                padding: 15px;
                padding-top: 35px;
                background-color: {self.theme.get('bg_card')};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top right;
                padding: 8px 16px;
                background-color: {self.theme.get('primary')};
                color: white;
                border-radius: 10px;
                font-size: 13px;
                margin-top: 2px;
            }}
            QTableWidget {{
                border: 1px solid {self.theme.get('border_light')};
                border-radius: 10px;
                background-color: {self.theme.get('bg_input')};
                gridline-color: {self.theme.get('border_light')};
                selection-background-color: {self.theme.get('primary_alpha')};
            }}
            QTableWidget::item {{
                padding: 8px;
                color: {self.theme.get('text_primary')};
            }}
            QTableWidget::item:selected {{
                background-color: {self.theme.get('primary')};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {self.theme.get('bg_tertiary')};
                color: {self.theme.get('text_primary')};
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {self.theme.get('primary')};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.get('primary_light')};
            }}
            QPushButton:pressed {{
                background-color: {self.theme.get('primary_dark')};
            }}
            QPushButton[class="danger"] {{
                background-color: {self.theme.get('error')};
            }}
            QPushButton[class="danger"]:hover {{
                background-color: #DC2626;
            }}
            QPushButton[class="secondary"] {{
                background-color: {self.theme.get('secondary')};
            }}
            QPushButton[class="secondary"]:hover {{
                background-color: {self.theme.get('secondary_dark')};
            }}
            QLineEdit, QSpinBox {{
                border: 2px solid {self.theme.get('border_light')};
                border-radius: 10px;
                padding: 10px 14px;
                background-color: {self.theme.get('bg_input')};
                color: {self.theme.get('text_primary')};
                font-size: 13px;
            }}
            QLineEdit:focus, QSpinBox:focus {{
                border-color: {self.theme.get('primary')};
            }}
            QTextEdit {{
                border: 2px solid {self.theme.get('border_light')};
                border-radius: 10px;
                padding: 10px;
                background-color: {self.theme.get('bg_input')};
                color: {self.theme.get('text_primary')};
            }}
            QCheckBox {{
                color: {self.theme.get('text_primary')};
                spacing: 12px;
                padding: 8px 4px;
                font-size: 13px;
                min-height: 30px;
            }}
            QCheckBox::indicator {{
                width: 22px;
                height: 22px;
                border-radius: 6px;
                border: 2px solid {self.theme.get('border_medium')};
                background-color: {self.theme.get('bg_input')};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.theme.get('primary')};
                border-color: {self.theme.get('primary')};
            }}
            QCheckBox::indicator:hover {{
                border-color: {self.theme.get('primary_light')};
            }}
            QTabWidget::pane {{
                border: none;
                background-color: transparent;
            }}
            QTabBar::tab {{
                background-color: {self.theme.get('bg_tertiary')};
                color: {self.theme.get('text_secondary')};
                border: none;
                padding: 12px 20px;
                margin-right: 4px;
                border-radius: 10px 10px 0 0;
                font-weight: 600;
                font-size: 13px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.theme.get('primary')};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {self.theme.get('bg_hover')};
            }}
        """)

    def setup_ui(self):
        """Setup main UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()
        
        header_label = QLabel("⚙️ تنظیمات پیشرفته")
        header_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header_label.setStyleSheet(f"color: {self.theme.get('text_primary')};")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        layout.addLayout(header_layout)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)

        # Create tabs
        self.setup_menu_tab()
        self.setup_tables_tab()
        self.setup_loyalty_tab()
        self.setup_general_tab()

        # Bottom buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        save_btn = QPushButton("💾 ذخیره تغییرات")
        save_btn.setProperty("class", "secondary")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_changes)
        buttons_layout.addWidget(save_btn)

        buttons_layout.addStretch()

        cancel_btn = QPushButton("❌ انصراف")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme.get('text_tertiary')};
            }}
            QPushButton:hover {{
                background-color: {self.theme.get('text_secondary')};
            }}
        """)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

    def setup_menu_tab(self):
        """Setup menu management tab with full CRUD"""
        menu_tab = QWidget()
        layout = QVBoxLayout(menu_tab)
        layout.setSpacing(15)

        # Menu items table
        menu_group = QGroupBox("📋 مدیریت آیتم‌های منو")
        menu_layout = QVBoxLayout(menu_group)
        menu_layout.setSpacing(12)

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍")
        search_label.setStyleSheet("font-size: 16px;")
        search_layout.addWidget(search_label)
        
        self.menu_search = QLineEdit()
        self.menu_search.setPlaceholderText("جستجو در منو...")
        self.menu_search.textChanged.connect(self.filter_menu_items)
        search_layout.addWidget(self.menu_search)
        menu_layout.addLayout(search_layout)

        # Table
        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(5)
        self.menu_table.setHorizontalHeaderLabels(["ID", "نام محصول", "قیمت (تومان)", "دسته‌بندی", "وضعیت"])
        self.menu_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.menu_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.menu_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.menu_table.setAlternatingRowColors(True)
        menu_layout.addWidget(self.menu_table)

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        add_btn = QPushButton("➕ افزودن محصول")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_menu_item)
        controls_layout.addWidget(add_btn)

        edit_btn = QPushButton("✏️ ویرایش")
        edit_btn.setStyleSheet(f"background-color: {self.theme.get('accent')};")
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.clicked.connect(self.edit_menu_item)
        controls_layout.addWidget(edit_btn)

        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setProperty("class", "danger")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_menu_item)
        controls_layout.addWidget(delete_btn)

        controls_layout.addStretch()

        toggle_btn = QPushButton("🔄 تغییر وضعیت")
        toggle_btn.setCursor(Qt.PointingHandCursor)
        toggle_btn.clicked.connect(self.toggle_product_status)
        controls_layout.addWidget(toggle_btn)

        menu_layout.addLayout(controls_layout)
        layout.addWidget(menu_group)

        # Category management
        cat_group = QGroupBox("📂 مدیریت دسته‌بندی‌ها")
        cat_layout = QHBoxLayout(cat_group)
        
        self.category_list = QComboBox()
        self.category_list.setMinimumWidth(150)
        self.load_categories()
        cat_layout.addWidget(self.category_list)
        
        add_cat_btn = QPushButton("➕ دسته جدید")
        add_cat_btn.setCursor(Qt.PointingHandCursor)
        add_cat_btn.clicked.connect(self.add_category)
        cat_layout.addWidget(add_cat_btn)
        
        cat_layout.addStretch()
        
        layout.addWidget(cat_group)

        self.tabs.addTab(menu_tab, "🍽️ مدیریت منو")

    def setup_tables_tab(self):
        """Setup tables management tab with visual grid"""
        tables_tab = QWidget()
        layout = QVBoxLayout(tables_tab)
        layout.setSpacing(15)

        # Tables count setting
        count_group = QGroupBox("🔢 تنظیمات تعداد میزها")
        count_layout = QHBoxLayout(count_group)

        count_layout.addWidget(QLabel("تعداد میزها:"))
        
        self.tables_count_spin = QSpinBox()
        self.tables_count_spin.setMinimum(1)
        self.tables_count_spin.setMaximum(100)
        self.tables_count_spin.setValue(20)
        self.tables_count_spin.setMinimumWidth(100)
        self.tables_count_spin.valueChanged.connect(self.update_tables_grid)
        count_layout.addWidget(self.tables_count_spin)
        
        count_layout.addStretch()
        
        apply_count_btn = QPushButton("✅ اعمال تغییرات")
        apply_count_btn.setProperty("class", "secondary")
        apply_count_btn.setCursor(Qt.PointingHandCursor)
        apply_count_btn.clicked.connect(self.apply_tables_count)
        count_layout.addWidget(apply_count_btn)

        layout.addWidget(count_group)

        # Tables visual grid
        tables_group = QGroupBox("🪑 نقشه میزها و وضعیت سفارشات")
        tables_group_layout = QVBoxLayout(tables_group)
        tables_group_layout.setContentsMargins(10, 30, 10, 10)

        # Scroll area for tables grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{ 
                border: none; 
                background-color: {self.theme.get('bg_secondary')};
                border-radius: 10px;
            }}
        """)
        
        self.tables_container = QWidget()
        self.tables_container.setStyleSheet(f"background-color: {self.theme.get('bg_secondary')};")
        self.tables_grid = QGridLayout(self.tables_container)
        self.tables_grid.setSpacing(15)
        self.tables_grid.setContentsMargins(15, 15, 15, 15)
        
        scroll.setWidget(self.tables_container)
        tables_group_layout.addWidget(scroll)

        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.addWidget(self._create_legend_item("🟢", "خالی"))
        legend_layout.addWidget(self._create_legend_item("🟡", "در حال سفارش"))
        legend_layout.addWidget(self._create_legend_item("🔴", "سفارش آماده"))
        legend_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 بروزرسانی وضعیت")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_tables_status)
        legend_layout.addWidget(refresh_btn)
        
        tables_group_layout.addLayout(legend_layout)
        layout.addWidget(tables_group, 1)

        self.tabs.addTab(tables_tab, "🪑 مدیریت میزها")
        
        # Initial grid creation
        self.update_tables_grid()

    def _create_legend_item(self, emoji, text):
        """Create legend item widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 15, 0)
        
        label = QLabel(f"{emoji} {text}")
        label.setStyleSheet(f"font-size: 12px; color: {self.theme.get('text_secondary')};")
        layout.addWidget(label)
        
        return widget

    def update_tables_grid(self):
        """Update visual tables grid"""
        # Clear existing
        while self.tables_grid.count():
            item = self.tables_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        count = self.tables_count_spin.value()
        cols = 5  # 5 columns
        
        for i in range(count):
            row = i // cols
            col = i % cols
            
            table_num = i + 1
            order_count = self.table_orders.get(table_num, 0)
            
            # Create table card
            card = self._create_table_card(table_num, order_count)
            self.tables_grid.addWidget(card, row, col)

    def _create_table_card(self, table_num, order_count):
        """Create a beautiful table card widget showing table status and order count"""
        # Determine status
        if order_count == 0:
            status_color = "#22C55E"  # Green - empty
            status_bg = "#DCFCE7"
            status_text = "خالی"
            icon = "🪑"
        elif order_count < 5:
            status_color = "#F59E0B"  # Orange/Yellow - ordering
            status_bg = "#FEF3C7"
            status_text = "سفارش‌دهی"
            icon = "🍽️"
        else:
            status_color = "#EF4444"  # Red - busy
            status_bg = "#FEE2E2"
            status_text = "شلوغ"
            icon = "🔥"
        
        # Card container
        card = QFrame()
        card.setFixedSize(140, 100)
        card.setFrameShape(QFrame.Shape.NoFrame)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.get('bg_card')},
                    stop:1 {self.theme.get('bg_secondary')});
                border: 2px solid {status_color};
                border-radius: 16px;
            }}
            QFrame:hover {{
                border-width: 3px;
                background: {self.theme.get('bg_hover')};
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)
        
        # Table icon and number
        header = QLabel(f"{icon} میز {table_num}")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"""
            font-weight: bold; 
            font-size: 15px; 
            color: {self.theme.get('text_primary')};
        """)
        layout.addWidget(header)
        
        # Status badge
        status_label = QLabel(status_text)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(24)
        status_label.setStyleSheet(f"""
            font-size: 11px; 
            font-weight: bold;
            color: {status_color}; 
            background-color: {status_bg};
            border-radius: 8px;
            padding: 3px 8px;
        """)
        layout.addWidget(status_label)
        
        # Order count
        if order_count > 0:
            count_label = QLabel(f"📦 {order_count} سفارش")
            count_label.setAlignment(Qt.AlignCenter)
            count_label.setStyleSheet(f"""
                font-size: 11px; 
                color: {self.theme.get('text_secondary')};
            """)
            layout.addWidget(count_label)
        
        return card

    def setup_loyalty_tab(self):
        """Setup customer loyalty program tab"""
        loyalty_tab = QWidget()
        layout = QVBoxLayout(loyalty_tab)
        layout.setSpacing(15)

        # Program settings
        program_group = QGroupBox("⭐ تنظیمات باشگاه مشتریان")
        program_layout = QVBoxLayout(program_group)

        self.loyalty_enabled = QCheckBox("فعال کردن باشگاه مشتریان")
        self.loyalty_enabled.setChecked(True)
        program_layout.addWidget(self.loyalty_enabled)

        # Points system
        points_layout = QGridLayout()
        points_layout.setSpacing(10)
        
        points_layout.addWidget(QLabel("امتیاز به ازای هر 1000 تومان:"), 0, 0)
        self.points_per_toman = QSpinBox()
        self.points_per_toman.setRange(1, 100)
        self.points_per_toman.setValue(10)
        points_layout.addWidget(self.points_per_toman, 0, 1)
        
        points_layout.addWidget(QLabel("ارزش هر امتیاز (تومان):"), 1, 0)
        self.points_value = QSpinBox()
        self.points_value.setRange(1, 1000)
        self.points_value.setValue(100)
        points_layout.addWidget(self.points_value, 1, 1)
        
        program_layout.addLayout(points_layout)
        layout.addWidget(program_group)

        # Customer management
        customers_group = QGroupBox("👥 مشتریان ثبت‌شده")
        customers_layout = QVBoxLayout(customers_group)

        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(4)
        self.customers_table.setHorizontalHeaderLabels(["نام", "شماره تماس", "امتیاز", "سطح"])
        self.customers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.customers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        customers_layout.addWidget(self.customers_table)

        customer_controls = QHBoxLayout()
        
        add_customer_btn = QPushButton("👤 افزودن مشتری")
        add_customer_btn.setCursor(Qt.PointingHandCursor)
        add_customer_btn.clicked.connect(self.add_customer)
        customer_controls.addWidget(add_customer_btn)
        
        edit_customer_btn = QPushButton("✏️ ویرایش")
        edit_customer_btn.setStyleSheet(f"background-color: {self.theme.get('accent')};")
        edit_customer_btn.setCursor(Qt.PointingHandCursor)
        edit_customer_btn.clicked.connect(self.edit_customer)
        customer_controls.addWidget(edit_customer_btn)
        
        customer_controls.addStretch()
        
        customers_layout.addLayout(customer_controls)
        layout.addWidget(customers_group, 1)

        self.tabs.addTab(loyalty_tab, "⭐ باشگاه مشتریان")

    def setup_general_tab(self):
        """Setup general settings tab"""
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)
        layout.setSpacing(15)

        # Business info
        business_group = QGroupBox("🏪 اطلاعات کسب‌وکار")
        business_layout = QFormLayout(business_group)
        business_layout.setSpacing(12)

        self.business_name = QLineEdit("کافه نمونه")
        business_layout.addRow("نام کافه:", self.business_name)

        self.business_address = QLineEdit("تهران، خیابان ولیعصر")
        business_layout.addRow("آدرس:", self.business_address)

        self.business_phone = QLineEdit("021-12345678")
        business_layout.addRow("تلفن:", self.business_phone)

        layout.addWidget(business_group)

        # Display settings
        display_group = QGroupBox("🖥️ تنظیمات نمایش")
        display_layout = QVBoxLayout(display_group)
        display_layout.setSpacing(8)
        display_layout.setContentsMargins(15, 25, 15, 15)

        self.dual_mode_enabled = QCheckBox("فعال کردن حالت دوپنل (آشپزخانه)")
        display_layout.addWidget(self.dual_mode_enabled)

        self.auto_kitchen_update = QCheckBox("بروزرسانی خودکار نمایش آشپزخانه")
        self.auto_kitchen_update.setChecked(True)
        display_layout.addWidget(self.auto_kitchen_update)

        self.show_prices = QCheckBox("نمایش قیمت‌ها در کارت محصولات")
        self.show_prices.setChecked(True)
        display_layout.addWidget(self.show_prices)

        layout.addWidget(display_group)

        # Receipt settings
        receipt_group = QGroupBox("🧾 تنظیمات فاکتور")
        receipt_layout = QVBoxLayout(receipt_group)

        receipt_layout.addWidget(QLabel("متن پاورقی فاکتور:"))
        self.receipt_footer = QTextEdit()
        self.receipt_footer.setPlainText(
            "با تشکر از انتخاب شما!\n"
            "آدرس: تهران، خیابان ولیعصر\n"
            "تلفن: 021-12345678"
        )
        self.receipt_footer.setMaximumHeight(80)
        receipt_layout.addWidget(self.receipt_footer)

        layout.addWidget(receipt_group)

        # System settings
        system_group = QGroupBox("⚡ تنظیمات سیستم")
        system_layout = QVBoxLayout(system_group)
        system_layout.setSpacing(8)
        system_layout.setContentsMargins(15, 25, 15, 15)

        self.auto_backup = QCheckBox("پشتیبان‌گیری خودکار روزانه")
        self.auto_backup.setChecked(True)
        system_layout.addWidget(self.auto_backup)

        self.confirm_delete = QCheckBox("تأیید قبل از حذف آیتم‌ها")
        self.confirm_delete.setChecked(True)
        system_layout.addWidget(self.confirm_delete)

        self.sound_enabled = QCheckBox("پخش صدا برای سفارش جدید")
        self.sound_enabled.setChecked(True)
        system_layout.addWidget(self.sound_enabled)

        layout.addWidget(system_group)

        layout.addStretch()
        self.tabs.addTab(general_tab, "🔧 تنظیمات عمومی")

    # ========== Data Loading ==========

    def load_current_settings(self):
        """Load current settings"""
        self.load_menu_items()
        self.load_customers()
        self.simulate_table_orders()

    def load_menu_items(self):
        """Load menu items into table"""
        products = self.menu_service.get_active_products()
        all_products = list(products)
        
        # Also get inactive products
        try:
            inactive = self.menu_service.get_all_products()
            all_products = list(inactive)
        except:
            pass

        self.menu_table.setRowCount(len(all_products))
        for row, product in enumerate(all_products):
            self.menu_table.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.menu_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.menu_table.setItem(row, 2, QTableWidgetItem(f"{product.price:,}"))
            self.menu_table.setItem(row, 3, QTableWidgetItem(product.category))
            
            status_item = QTableWidgetItem("✅ فعال" if product.is_active else "❌ غیرفعال")
            status_item.setForeground(
                Qt.GlobalColor.darkGreen if product.is_active else Qt.GlobalColor.red
            )
            self.menu_table.setItem(row, 4, status_item)

        self.menu_table.resizeColumnsToContents()
        self.menu_table.setColumnWidth(0, 50)

    def load_categories(self):
        """Load categories into combo box"""
        self.category_list.clear()
        categories = self.menu_service.get_categories()
        self.category_list.addItems(sorted(categories))

    def load_customers(self):
        """Load customer data"""
        sample_customers = [
            ["احمد رضایی", "09123456789", "150", "🥉 سطح 1"],
            ["مریم احمدی", "09198765432", "450", "🥈 سطح 2"],
            ["علی محمدی", "09155556666", "850", "🥇 VIP"]
        ]

        self.customers_table.setRowCount(len(sample_customers))
        for row, customer in enumerate(sample_customers):
            for col, data in enumerate(customer):
                self.customers_table.setItem(row, col, QTableWidgetItem(data))

        self.customers_table.resizeColumnsToContents()

    def simulate_table_orders(self):
        """Simulate table orders for demo"""
        import random
        for i in range(1, self.tables_count_spin.value() + 1):
            self.table_orders[i] = random.choice([0, 0, 0, 1, 2, 3, 5, 7])
        self.update_tables_grid()

    # ========== Actions ==========

    def filter_menu_items(self):
        """Filter menu items by search text"""
        search_text = self.menu_search.text().lower()
        for row in range(self.menu_table.rowCount()):
            match = False
            for col in range(self.menu_table.columnCount()):
                item = self.menu_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.menu_table.setRowHidden(row, not match)

    def add_menu_item(self):
        """Add new menu item"""
        from ui.add_product_dialog import AddProductDialog
        dialog = AddProductDialog(self)
        if dialog.exec():
            self.load_menu_items()
            self.load_categories()
            QMessageBox.information(self, "موفق", "✅ محصول جدید با موفقیت اضافه شد!")

    def edit_menu_item(self):
        """Edit selected menu item"""
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "⚠️ لطفاً یک محصول را انتخاب کنید")
            return

        product_id = self.menu_table.item(current_row, 0).text()
        product_name = self.menu_table.item(current_row, 1).text()
        
        # Simple edit dialog
        from PySide6.QtWidgets import QInputDialog
        new_price, ok = QInputDialog.getInt(
            self, "ویرایش قیمت", 
            f"قیمت جدید برای '{product_name}':",
            int(self.menu_table.item(current_row, 2).text().replace(",", "")),
            1000, 10000000
        )
        
        if ok:
            try:
                self.menu_service.update_product_price(int(product_id), new_price)
                self.load_menu_items()
                QMessageBox.information(self, "موفق", "✅ قیمت محصول بروزرسانی شد!")
            except Exception as e:
                QMessageBox.warning(self, "خطا", f"❌ خطا در بروزرسانی: {e}")

    def delete_menu_item(self):
        """Delete selected menu item"""
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "⚠️ لطفاً یک محصول را انتخاب کنید")
            return

        product_name = self.menu_table.item(current_row, 1).text()

        if self.confirm_delete.isChecked():
            reply = QMessageBox.question(
                self, "تأیید حذف",
                f"آیا مطمئن هستید که محصول '{product_name}' را حذف کنید؟",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        try:
            product_id = int(self.menu_table.item(current_row, 0).text())
            self.menu_service.deactivate_product(product_id)
            self.load_menu_items()
            QMessageBox.information(self, "موفق", f"✅ محصول '{product_name}' غیرفعال شد!")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"❌ خطا در حذف: {e}")

    def toggle_product_status(self):
        """Toggle product active status"""
        current_row = self.menu_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "⚠️ لطفاً یک محصول را انتخاب کنید")
            return

        product_id = int(self.menu_table.item(current_row, 0).text())
        product_name = self.menu_table.item(current_row, 1).text()
        current_status = "فعال" in self.menu_table.item(current_row, 4).text()

        try:
            if current_status:
                self.menu_service.deactivate_product(product_id)
            else:
                self.menu_service.activate_product(product_id)
            
            self.load_menu_items()
            new_status = "غیرفعال" if current_status else "فعال"
            QMessageBox.information(self, "موفق", f"✅ محصول '{product_name}' {new_status} شد!")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"❌ خطا: {e}")

    def add_category(self):
        """Add new category"""
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "دسته‌بندی جدید", "نام دسته‌بندی:")
        if ok and name:
            self.category_list.addItem(name)
            QMessageBox.information(self, "موفق", f"✅ دسته‌بندی '{name}' اضافه شد!")

    def apply_tables_count(self):
        """Apply new tables count"""
        count = self.tables_count_spin.value()
        self.tables_count = count
        self.update_tables_grid()
        QMessageBox.information(self, "موفق", f"✅ تعداد میزها به {count} تغییر یافت!")

    def refresh_tables_status(self):
        """Refresh tables status"""
        self.simulate_table_orders()
        QMessageBox.information(self, "بروزرسانی", "✅ وضعیت میزها بروزرسانی شد!")

    def add_customer(self):
        """Add new customer"""
        from ui.add_customer_dialog import AddCustomerDialog
        dialog = AddCustomerDialog(self)
        if dialog.exec():
            self.load_customers()
            QMessageBox.information(self, "موفق", "✅ مشتری جدید اضافه شد!")

    def edit_customer(self):
        """Edit selected customer"""
        current_row = self.customers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "خطا", "⚠️ لطفاً یک مشتری را انتخاب کنید")
            return

        customer_name = self.customers_table.item(current_row, 0).text()
        QMessageBox.information(self, "توجه", f"ویرایش مشتری '{customer_name}' در نسخه‌های بعدی اضافه خواهد شد.")

    def save_changes(self):
        """Save all changes"""
        # Update parent window if exists
        if self.parent():
            try:
                # Update table combo in parent
                parent = self.parent()
                if hasattr(parent, 'table_combo'):
                    current = parent.table_combo.currentIndex()
                    parent.table_combo.clear()
                    parent.table_combo.addItems([f"میز {i}" for i in range(1, self.tables_count_spin.value() + 1)])
                    parent.table_combo.addItem("بیرون بر")
                    if current < parent.table_combo.count():
                        parent.table_combo.setCurrentIndex(current)
                
                # Reload menu if method exists
                if hasattr(parent, 'load_menu_data'):
                    parent.load_menu_data()
            except:
                pass

        QMessageBox.information(self, "موفق", "✅ تنظیمات با موفقیت ذخیره شد!")
        self.accept()
