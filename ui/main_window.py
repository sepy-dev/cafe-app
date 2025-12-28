# main_window.py - Clean POS-style main window
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QFrame, QScrollArea, QTabWidget,
    QListWidget, QSpinBox, QMessageBox, QLineEdit, QSplitter, QGroupBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
from datetime import datetime

from application.order_service import OrderService
from application.menu_service import MenuService
from ui.styles import POSStyles, FontManager, POSTheme


class KitchenDisplayWidget(QWidget):
    """Kitchen display widget for dual monitor setup"""

    def __init__(self, order_service, parent=None):
        super().__init__(parent)
        self.order_service = order_service
        self.current_orders = {}  # table_number -> order_items
        self.last_order_count = 0

        # Sound effect for new orders
        self.new_order_sound = None

        self.setWindowTitle("🍳 نمایش آشپزخانه")
        self.resize(800, 600)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {POSTheme.BG_SECONDARY};
                color: {POSTheme.TEXT_PRIMARY};
                font-size: 14px;
            }}
        """)

        layout = QVBoxLayout(self)

        # Header
        header = QLabel("🍳 سفارشات آشپزخانه")
        header.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {POSTheme.PRIMARY};
                padding: 20px;
                background-color: {POSTheme.PRIMARY};
                color: white;
                text-align: center;
            }}
        """)
        layout.addWidget(header)

        # Orders display area
        self.orders_scroll = QScrollArea()
        self.orders_scroll.setWidgetResizable(True)
        self.orders_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self.orders_container = QWidget()
        self.orders_layout = QVBoxLayout(self.orders_container)
        self.orders_layout.setSpacing(15)

        self.orders_scroll.setWidget(self.orders_container)
        layout.addWidget(self.orders_scroll, 1)

        # Status bar with stats
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(10, 5, 10, 5)

        self.status_label = QLabel("آماده دریافت سفارشات...")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {POSTheme.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """)
        status_layout.addWidget(self.status_label)

        status_layout.addStretch()

        # Real-time stats
        self.stats_label = QLabel("📊 آمار: ۰ سفارش فعال")
        self.stats_label.setStyleSheet(f"""
            QLabel {{
                color: {POSTheme.PRIMARY};
                font-weight: bold;
                font-size: 12px;
            }}
        """)
        status_layout.addWidget(self.stats_label)

        status_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {POSTheme.BG_MAIN};
                border-top: 2px solid {POSTheme.BORDER_LIGHT};
            }}
        """)
        layout.addWidget(status_widget)

        # Timer for updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_orders)
        self.update_timer.start(2000)  # Update every 2 seconds

        self.update_orders()

    def update_orders(self):
        """Update orders display"""
        # Clear existing orders
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Get all active orders (for demo, we'll simulate some orders)
        # In real implementation, this would come from a shared order queue
        from datetime import datetime, timedelta
        import random

        base_time = datetime.now()
        sample_orders = [
            {"table": 1, "items": [("قهوه", 2), ("کیک", 1)], "time": (base_time - timedelta(minutes=random.randint(5, 15))).strftime("%H:%M"), "status": "آماده‌سازی"},
            {"table": 3, "items": [("چای", 1), ("ساندویچ", 1)], "time": (base_time - timedelta(minutes=random.randint(3, 10))).strftime("%H:%M"), "status": "در حال پخت"},
            {"table": 5, "items": [("لاته", 3)], "time": (base_time - timedelta(minutes=random.randint(1, 5))).strftime("%H:%M"), "status": "آماده‌سازی"},
        ]

        # Update status and stats
        active_orders = len(sample_orders)
        total_items = sum(len(order['items']) for order in sample_orders)

        # Check for new orders and play sound
        if active_orders > self.last_order_count and self.last_order_count > 0:
            self.play_new_order_sound()

        self.last_order_count = active_orders

        if sample_orders:
            self.status_label.setText(f"📋 {active_orders} سفارش فعال")
            self.stats_label.setText(f"📊 آمار: {active_orders} سفارش، {total_items} آیتم")
        else:
            self.status_label.setText("✅ سفارش فعالی وجود ندارد")
            self.stats_label.setText("📊 آمار: ۰ سفارش، ۰ آیتم")

        for order in sample_orders:
            order_card = self.create_order_card(order)
            self.orders_layout.addWidget(order_card)

        self.orders_layout.addStretch()

    def create_order_card(self, order):
        """Create order card for kitchen display"""
        # Calculate wait time
        from datetime import datetime
        order_time = datetime.strptime(order['time'], "%H:%M")
        now = datetime.now()
        wait_minutes = (now - order_time.replace(year=now.year, month=now.month, day=now.day)).seconds // 60

        card = QGroupBox(f"میز {order['table']} - {order['time']} ({wait_minutes} دقیقه)")
        card.setStyleSheet(f"""
            QGroupBox {{
                background-color: {POSTheme.BG_MAIN};
                border: 3px solid {POSTheme.ACCENT if wait_minutes < 10 else '#EF4444'};
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }}
            QGroupBox::title {{
                color: {POSTheme.PRIMARY};
                font-weight: bold;
                font-size: 16px;
                padding: 5px;
            }}
        """)

        layout = QVBoxLayout(card)

        # Order items
        for item_name, quantity in order['items']:
            item_label = QLabel(f"• {item_name} × {quantity}")
            item_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    font-weight: bold;
                    color: {POSTheme.TEXT_PRIMARY};
                    padding: 3px 0;
                }}
            """)
            layout.addWidget(item_label)

        # Status and wait time
        status_layout = QHBoxLayout()

        status_label = QLabel(f"وضعیت: {order['status']}")
        status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {POSTheme.SECONDARY};
                font-weight: bold;
            }}
        """)
        status_layout.addWidget(status_label)

        # Priority indicator
        if wait_minutes > 15:
            priority_label = QLabel("🔴 فوری")
            priority_label.setStyleSheet("color: #EF4444; font-weight: bold;")
            status_layout.addWidget(priority_label)
        elif wait_minutes > 10:
            priority_label = QLabel("🟡 عجله")
            priority_label.setStyleSheet("color: #F59E0B; font-weight: bold;")
            status_layout.addWidget(priority_label)

        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Action buttons
        buttons_layout = QHBoxLayout()

        ready_btn = QPushButton("✅ آماده")
        ready_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {POSTheme.SECONDARY};
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        ready_btn.clicked.connect(lambda: self.mark_order_ready(order['table']))
        buttons_layout.addWidget(ready_btn)

        layout.addLayout(buttons_layout)

        return card

    def mark_order_ready(self, table_number):
        """Mark order as ready"""
        QMessageBox.information(self, "سفارش آماده",
                               f"سفارش میز {table_number} آماده تحویل است!")
        self.update_orders()

    def play_new_order_sound(self):
        """Play sound for new orders"""
        try:
            # Try to play system bell sound
            import winsound
            winsound.Beep(800, 500)  # Frequency 800Hz, duration 500ms
        except ImportError:
            # On non-Windows systems, we'll skip sound
            pass


class POSMainWindow(QMainWindow):
    """Clean POS-style main window for cafe ordering system with dual mode support"""

    def __init__(self):
        super().__init__()
        self.order_service = OrderService()
        self.menu_service = MenuService()

        # Initialize theme
        self.current_theme = {
            "name": "modern_blue",
            "PRIMARY": "#2563EB",
            "SECONDARY": "#10B981",
            "ACCENT": "#F59E0B",
            "BG_MAIN": "#FFFFFF",
            "BG_SECONDARY": "#F8FAFC",
            "TEXT_PRIMARY": "#1E293B",
            "TEXT_SECONDARY": "#64748B"
        }

        # Dual mode settings
        self.dual_mode = False
        self.kitchen_display = None

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
        self.header_widget = QWidget()
        self.header_widget.setProperty("class", "header")
        self.header_widget.setFixedHeight(80)  # Fixed height for better appearance
        header_layout = QHBoxLayout(self.header_widget)
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

        # Customer selection
        customer_layout = QVBoxLayout()
        customer_layout.setSpacing(2)

        customer_label = QLabel("مشتری")
        customer_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold;")
        customer_layout.addWidget(customer_label)

        customer_select_layout = QHBoxLayout()
        self.customer_combo = QComboBox()
        self.customer_combo.addItem("👤 انتخاب مشتری", "")
        self.customer_combo.addItem("احمد رضایی (150 امتیاز)", "ahmad")
        self.customer_combo.addItem("مریم احمدی (450 امتیاز)", "maryam")
        self.customer_combo.addItem("علی محمدی (VIP)", "ali")
        self.customer_combo.currentIndexChanged.connect(self.on_customer_changed)
        self.customer_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.9);
                color: #1E293B;
                border: none;
                border-radius: 6px;
                padding: 6px;
                min-width: 140px;
                font-size: 11px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)
        customer_select_layout.addWidget(self.customer_combo)

        add_customer_btn = QPushButton("+")
        add_customer_btn.setToolTip("افزودن مشتری جدید")
        add_customer_btn.clicked.connect(self.add_new_customer)
        add_customer_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        customer_select_layout.addWidget(add_customer_btn)

        customer_layout.addLayout(customer_select_layout)
        controls_layout.addLayout(customer_layout)

        # Dual mode button
        dual_btn = QPushButton("🍳" if not self.dual_mode else "💻")
        dual_btn.setToolTip("حالت دوپنل (آشپزخانه)")
        dual_btn.clicked.connect(self.toggle_dual_mode)
        dual_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,165,0,0.8);
                color: white;
                border: 1px solid rgba(255,165,0,0.5);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255,165,0,0.9);
                border-color: rgba(255,165,0,0.7);
            }
        """)
        controls_layout.addWidget(dual_btn)

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
        products_layout.addWidget(self.header_widget)

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

                # Notify kitchen display if in dual mode
                if self.dual_mode and self.kitchen_display:
                    self.kitchen_display.update_orders()

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

    def toggle_dual_mode(self):
        """Toggle between single and dual monitor mode"""
        self.dual_mode = not self.dual_mode

        if self.dual_mode:
            self.create_dual_layout()
            self.show_notification("حالت دوپنل فعال شد", "نمایش آشپزخانه باز شده است", "🍳")
        else:
            self.create_single_layout()
            if self.kitchen_display:
                self.kitchen_display.close()
                self.kitchen_display = None
            self.show_notification("حالت تک‌پنل فعال شد", "به حالت عادی بازگشتیم", "💻")

    def create_dual_layout(self):
        """Create dual monitor layout with splitter"""
        # Close existing kitchen display if any
        if self.kitchen_display:
            self.kitchen_display.close()

        # Create new kitchen display
        self.kitchen_display = KitchenDisplayWidget(self.order_service)
        self.kitchen_display.show()

        # Move kitchen display to second monitor if available
        screens = self.screen().availableGeometry()
        if len(self.screens()) > 1:
            # Move to second screen
            second_screen = self.screens()[1].availableGeometry()
            self.kitchen_display.move(second_screen.x(), second_screen.y())
            self.kitchen_display.resize(second_screen.width(), second_screen.height())
        else:
            # Move to right side of current screen
            self.kitchen_display.move(self.x() + self.width() + 10, self.y())

        self.resize(1000, 900)  # Make main window smaller for dual mode

    def create_single_layout(self):
        """Return to single monitor layout"""
        self.resize(1400, 900)  # Restore original size

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

    def update_header_colors(self):
        """Update header colors based on current theme"""
        header_bg = self.current_theme["PRIMARY"]
        text_color = "white"

        # Update header background
        header_style = f"""
            QWidget[class="header"] {{
                background-color: {header_bg};
                color: {text_color};
                padding: 16px;
                border-radius: 0px;
            }}
        """
        self.header_widget.setStyleSheet(header_style)

        # Update table indicator colors
        if hasattr(self, 'table_indicator'):
            if self.order_service.get_table_number() is None:
                indicator_bg = "#FFA500"
            else:
                indicator_bg = "#FFD700"

            indicator_style = f"""
                QLabel {{
                    font-size: 16px;
                    font-weight: bold;
                    color: {self.current_theme['TEXT_PRIMARY']};
                    background-color: {indicator_bg};
                    padding: 8px 16px;
                    border-radius: 20px;
                    border: 2px solid rgba(255,255,255,0.3);
                }}
            """
            self.table_indicator.setStyleSheet(indicator_style)

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
        """Apply a specific theme with proper updates"""
        # Update theme constants
        if theme_name == "modern_blue":
            self.current_theme = {
                "name": "modern_blue",
                "PRIMARY": "#2563EB",
                "SECONDARY": "#10B981",
                "ACCENT": "#F59E0B",
                "BG_MAIN": "#FFFFFF",
                "BG_SECONDARY": "#F8FAFC",
                "TEXT_PRIMARY": "#1E293B",
                "TEXT_SECONDARY": "#64748B"
            }
        elif theme_name == "dark":
            self.current_theme = {
                "name": "dark",
                "PRIMARY": "#6366F1",
                "SECONDARY": "#8B5CF6",
                "ACCENT": "#F59E0B",
                "BG_MAIN": "#1F2937",
                "BG_SECONDARY": "#111827",
                "TEXT_PRIMARY": "#F9FAFB",
                "TEXT_SECONDARY": "#D1D5DB"
            }
        elif theme_name == "warm_orange":
            self.current_theme = {
                "name": "warm_orange",
                "PRIMARY": "#EA580C",
                "SECONDARY": "#059669",
                "ACCENT": "#DC2626",
                "BG_MAIN": "#FFFFFF",
                "BG_SECONDARY": "#FFF7ED",
                "TEXT_PRIMARY": "#1E293B",
                "TEXT_SECONDARY": "#64748B"
            }

        # Update global theme
        POSTheme.PRIMARY = self.current_theme["PRIMARY"]
        POSTheme.SECONDARY = self.current_theme["SECONDARY"]
        POSTheme.ACCENT = self.current_theme["ACCENT"]
        POSTheme.BG_MAIN = self.current_theme["BG_MAIN"]
        POSTheme.BG_SECONDARY = self.current_theme["BG_SECONDARY"]
        POSTheme.TEXT_PRIMARY = self.current_theme["TEXT_PRIMARY"]
        POSTheme.TEXT_SECONDARY = self.current_theme["TEXT_SECONDARY"]

        # Reapply styles to entire application
        self.setStyleSheet(POSStyles.get_main_style())

        # Update header colors
        self.update_header_colors()

    def on_customer_changed(self):
        """Handle customer selection change"""
        customer_data = self.customer_combo.currentData()
        if customer_data:
            customer_name = self.customer_combo.currentText().split(" (")[0]
            self.show_notification("مشتری انتخاب شد", f"خوش آمدید {customer_name}!", "👤")
            self.current_customer = customer_data
        else:
            self.current_customer = None

    def add_new_customer(self):
        """Add new customer"""
        from ui.add_customer_dialog import AddCustomerDialog
        dialog = AddCustomerDialog(self)
        if dialog.exec():
            # Refresh customer list
            self.customer_combo.clear()
            self.customer_combo.addItem("👤 انتخاب مشتری", "")
            self.customer_combo.addItem("احمد رضایی (150 امتیاز)", "ahmad")
            self.customer_combo.addItem("مریم احمدی (450 امتیاز)", "maryam")
            self.customer_combo.addItem("علی محمدی (VIP)", "ali")
            # Add the new customer
            new_customer_name = dialog.name_input.text()
            self.customer_combo.addItem(f"{new_customer_name} (50 امتیاز)", "new")
            self.show_notification("مشتری اضافه شد", f"{new_customer_name} به باشگاه مشتریان اضافه شد!", "✅")

    def show_settings(self):
        """Show advanced settings dialog"""
        from ui.advanced_settings_dialog import AdvancedSettingsDialog
        dialog = AdvancedSettingsDialog(self)
        dialog.exec()