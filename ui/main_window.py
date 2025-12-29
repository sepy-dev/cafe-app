# main_window.py - Clean POS-style main window with Theme Support
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QFrame, QScrollArea, QTabWidget,
    QListWidget, QSpinBox, QMessageBox, QLineEdit, QSplitter, QGroupBox,
    QListWidgetItem
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
from datetime import datetime

from application.order_service import OrderService
from application.menu_service import MenuService
from ui.styles import ThemeManager, StyleGenerator, FontManager, ThemePresets


class KitchenDisplayWidget(QWidget):
    """Kitchen display widget for dual monitor setup"""

    def __init__(self, order_service, parent=None):
        super().__init__(parent)
        self.order_service = order_service
        self.theme_manager = ThemeManager()
        self.current_orders = {}
        self.last_order_count = 0
        self.new_order_sound = None

        self.setWindowTitle("🍳 نمایش آشپزخانه")
        self.resize(800, 600)
        self.apply_styles()
        self.setup_ui()
        
        # Timer for updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_orders)
        self.update_timer.start(2000)
        self.update_orders()
    
    def apply_styles(self):
        """Apply theme styles"""
        theme = self.theme_manager.current_theme
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_secondary')};
                color: {theme.get('text_primary')};
                font-size: 14px;
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
            }}
        """)
    
    def setup_ui(self):
        """Setup UI components"""
        theme = self.theme_manager.current_theme
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("🍳 سفارشات آشپزخانه")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                background-color: {theme.get('primary')};
                color: white;
            }}
        """)
        layout.addWidget(header)

        # Orders display area
        self.orders_scroll = QScrollArea()
        self.orders_scroll.setWidgetResizable(True)
        self.orders_scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.orders_container = QWidget()
        self.orders_layout = QVBoxLayout(self.orders_container)
        self.orders_layout.setSpacing(15)
        self.orders_layout.setContentsMargins(15, 15, 15, 15)

        self.orders_scroll.setWidget(self.orders_container)
        layout.addWidget(self.orders_scroll, 1)

        # Status bar
        status_widget = QWidget()
        status_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_main')};
                border-top: 2px solid {theme.get('border_light')};
            }}
        """)
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(15, 10, 15, 10)

        self.status_label = QLabel("آماده دریافت سفارشات...")
        self.status_label.setStyleSheet(f"color: {theme.get('text_secondary')}; font-size: 13px;")
        status_layout.addWidget(self.status_label)

        status_layout.addStretch()

        self.stats_label = QLabel("📊 آمار: ۰ سفارش فعال")
        self.stats_label.setStyleSheet(f"color: {theme.get('primary')}; font-weight: bold; font-size: 13px;")
        status_layout.addWidget(self.stats_label)

        layout.addWidget(status_widget)

    def update_orders(self):
        """Update orders display"""
        while self.orders_layout.count():
            item = self.orders_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        from datetime import datetime, timedelta
        import random

        base_time = datetime.now()
        sample_orders = [
            {"table": 1, "items": [("قهوه", 2), ("کیک", 1)], "time": (base_time - timedelta(minutes=random.randint(5, 15))).strftime("%H:%M"), "status": "آماده‌سازی"},
            {"table": 3, "items": [("چای", 1), ("ساندویچ", 1)], "time": (base_time - timedelta(minutes=random.randint(3, 10))).strftime("%H:%M"), "status": "در حال پخت"},
            {"table": 5, "items": [("لاته", 3)], "time": (base_time - timedelta(minutes=random.randint(1, 5))).strftime("%H:%M"), "status": "آماده‌سازی"},
        ]

        active_orders = len(sample_orders)
        total_items = sum(len(order['items']) for order in sample_orders)

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
        theme = self.theme_manager.current_theme
        
        order_time = datetime.strptime(order['time'], "%H:%M")
        now = datetime.now()
        wait_minutes = (now - order_time.replace(year=now.year, month=now.month, day=now.day)).seconds // 60

        border_color = theme.get('accent') if wait_minutes < 10 else theme.get('error')
        
        card = QGroupBox(f"میز {order['table']} - {order['time']} ({wait_minutes} دقیقه)")
        card.setStyleSheet(f"""
            QGroupBox {{
                background-color: {theme.get('bg_card')};
                border: 3px solid {border_color};
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                color: {theme.get('primary')};
                font-size: 16px;
                padding: 5px 10px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        for item_name, quantity in order['items']:
            item_label = QLabel(f"• {item_name} × {quantity}")
            item_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    font-weight: bold;
                    color: {theme.get('text_primary')};
                    padding: 3px 0;
                    background-color: transparent;
                }}
            """)
            layout.addWidget(item_label)

        status_layout = QHBoxLayout()

        status_label = QLabel(f"وضعیت: {order['status']}")
        status_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                color: {theme.get('secondary')};
                font-weight: bold;
                background-color: transparent;
            }}
        """)
        status_layout.addWidget(status_label)

        if wait_minutes > 15:
            priority_label = QLabel("🔴 فوری")
            priority_label.setStyleSheet(f"color: {theme.get('error')}; font-weight: bold; background-color: transparent;")
            status_layout.addWidget(priority_label)
        elif wait_minutes > 10:
            priority_label = QLabel("🟡 عجله")
            priority_label.setStyleSheet(f"color: {theme.get('warning')}; font-weight: bold; background-color: transparent;")
            status_layout.addWidget(priority_label)

        status_layout.addStretch()
        layout.addLayout(status_layout)

        buttons_layout = QHBoxLayout()

        ready_btn = QPushButton("✅ آماده")
        ready_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.get('secondary')};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {theme.get('secondary_dark')};
            }}
            QPushButton:pressed {{
                background-color: {theme.get('secondary_dark')};
            }}
        """)
        ready_btn.clicked.connect(lambda: self.mark_order_ready(order['table']))
        buttons_layout.addWidget(ready_btn)

        layout.addLayout(buttons_layout)

        return card

    def mark_order_ready(self, table_number):
        """Mark order as ready"""
        QMessageBox.information(self, "سفارش آماده", f"سفارش میز {table_number} آماده تحویل است!")
        self.update_orders()

    def play_new_order_sound(self):
        """Play sound for new orders"""
        try:
            import winsound
            winsound.Beep(800, 500)
        except ImportError:
            pass


class POSMainWindow(QMainWindow):
    """Clean POS-style main window for cafe ordering system"""

    def __init__(self):
        super().__init__()
        self.order_service = OrderService()
        self.menu_service = MenuService()
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # State variables
        self.dual_mode = False
        self.kitchen_display = None
        self.current_customer = None

        self.setWindowTitle("🍽️ سیستم ثبت سفارش کافه")
        self.resize(1400, 900)
        self.setMinimumSize(900, 600)  # Smaller minimum for better responsive

        # Apply theme and font
        self.apply_theme()
        self.setFont(FontManager.get_main_font())

        self.setup_ui()
        self.load_menu_data()
        self.setup_timers()
        self.setup_shortcuts()
    
    def get_theme_color(self, key: str) -> str:
        """Get color from current theme"""
        return self.theme_manager.get_color(key)
    
    def apply_theme(self):
        """Apply current theme to the window"""
        theme = self.theme_manager.current_theme
        stylesheet = StyleGenerator.generate_main_stylesheet(theme)
        self.setStyleSheet(stylesheet)
    
    def on_theme_changed(self, theme):
        """Handle theme change signal"""
        self.apply_theme()
        self.update_dynamic_styles()
    
    def update_dynamic_styles(self):
        """Update styles that aren't covered by main stylesheet"""
        theme = self.theme_manager.current_theme
        
        # Update header
        if hasattr(self, 'header_widget'):
            self.header_widget.setStyleSheet(f"""
                QWidget {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {theme.get('primary')},
                        stop:1 {theme.get('primary_light')});
                }}
            """)
        
        # Reload menu to update product cards
        if hasattr(self, 'category_tabs'):
            self.load_menu_data()

    def setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Left side - Products
        self.setup_products_section(main_layout)

        # Right side - Cart
        self.setup_cart_section(main_layout)

        # Initialize with default table
        self.on_table_changed()

    def setup_products_section(self, parent_layout):
        """Setup products section with categories"""
        theme = self.theme_manager.current_theme
        
        products_widget = QWidget()
        products_widget.setAttribute(Qt.WA_StyledBackground, True)
        products_layout = QVBoxLayout(products_widget)
        products_layout.setSpacing(10)
        products_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.header_widget = QWidget()
        self.header_widget.setProperty("class", "header")
        self.header_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.header_widget.setFixedHeight(85)
        self.header_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme.get('primary')},
                    stop:0.5 {theme.get('primary_light')},
                    stop:1 {theme.get('primary')});
                border-radius: 20px;
            }}
        """)
        
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(15, 10, 15, 10)
        header_layout.setSpacing(10)

        # Title
        title_widget = QWidget()
        title_widget.setAttribute(Qt.WA_StyledBackground, True)
        title_widget.setStyleSheet("background-color: transparent;")
        title_layout = QVBoxLayout(title_widget)
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("🍽️ سیستم ثبت سفارش کافه")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white; background-color: transparent;")
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("ساده، سریع و حرفه‌ای")
        subtitle_label.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.8); background-color: transparent;")
        title_layout.addWidget(subtitle_label)

        header_layout.addWidget(title_widget)
        header_layout.addStretch()

        # Table indicator
        table_indicator_widget = QWidget()
        table_indicator_widget.setAttribute(Qt.WA_StyledBackground, True)
        table_indicator_widget.setStyleSheet("background-color: transparent;")
        table_indicator_layout = QVBoxLayout(table_indicator_widget)
        table_indicator_layout.setSpacing(2)
        table_indicator_layout.setAlignment(Qt.AlignCenter)
        table_indicator_layout.setContentsMargins(0, 0, 0, 0)

        table_indicator_title = QLabel("میز فعلی")
        table_indicator_title.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold; background-color: transparent;")
        table_indicator_layout.addWidget(table_indicator_title)

        self.table_indicator = QLabel("میز ۱")
        self.table_indicator.setAttribute(Qt.WA_StyledBackground, True)
        self.table_indicator.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFD700;
                background-color: rgba(255,255,255,0.2);
                padding: 10px 20px;
                border-radius: 25px;
                border: 2px solid rgba(255,215,0,0.5);
            }
        """)
        table_indicator_layout.addWidget(self.table_indicator)

        header_layout.addWidget(table_indicator_widget)
        header_layout.addStretch()

        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        # Theme selector
        theme_widget = QWidget()
        theme_widget.setAttribute(Qt.WA_StyledBackground, True)
        theme_widget.setStyleSheet("background-color: transparent;")
        theme_layout = QVBoxLayout(theme_widget)
        theme_layout.setSpacing(2)
        theme_layout.setContentsMargins(0, 0, 0, 0)

        theme_label = QLabel("تم")
        theme_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold; background-color: transparent;")
        theme_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["🔵 آبی مدرن", "🌙 تاریک", "🟠 نارنجی", "☕ قهوه‌ای"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.35);
                border-radius: 12px;
                padding: 8px 12px;
                min-width: 115px;
                font-size: 12px;
                font-weight: 500;
            }
            QComboBox::drop-down { border: none; width: 25px; }
            QComboBox::down-arrow { border-top: 6px solid white; border-left: 4px solid transparent; border-right: 4px solid transparent; }
            QComboBox:hover { background-color: rgba(255,255,255,0.35); }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1E293B;
                border: 2px solid #2563EB;
                border-radius: 12px;
                padding: 6px;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px 14px;
                border-radius: 8px;
                margin: 2px;
                color: #1E293B;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: rgba(37, 99, 235, 0.12);
                color: #1E293B;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #2563EB;
                color: white;
            }
        """)
        theme_layout.addWidget(self.theme_combo)
        controls_layout.addWidget(theme_widget)

        # Table selector
        table_select_widget = QWidget()
        table_select_widget.setAttribute(Qt.WA_StyledBackground, True)
        table_select_widget.setStyleSheet("background-color: transparent;")
        table_select_layout = QVBoxLayout(table_select_widget)
        table_select_layout.setSpacing(2)
        table_select_layout.setContentsMargins(0, 0, 0, 0)

        table_select_label = QLabel("تغییر میز")
        table_select_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold; background-color: transparent;")
        table_select_layout.addWidget(table_select_label)

        self.table_combo = QComboBox()
        self.table_combo.addItems([f"میز {i}" for i in range(1, 21)])
        self.table_combo.addItem("بیرون بر")
        self.table_combo.currentIndexChanged.connect(self.on_table_changed)
        self.table_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.35);
                border-radius: 12px;
                padding: 8px 12px;
                min-width: 95px;
                font-size: 12px;
                font-weight: 500;
            }
            QComboBox::drop-down { border: none; width: 25px; }
            QComboBox:hover { background-color: rgba(255,255,255,0.35); }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1E293B;
                border: 2px solid #2563EB;
                border-radius: 12px;
                padding: 6px;
                selection-background-color: #2563EB;
                selection-color: white;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px 14px;
                border-radius: 8px;
                margin: 2px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: rgba(37, 99, 235, 0.15);
                color: #1E293B;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #2563EB;
                color: white;
            }
        """)
        table_select_layout.addWidget(self.table_combo)
        controls_layout.addWidget(table_select_widget)

        # Customer selector
        customer_widget = QWidget()
        customer_widget.setAttribute(Qt.WA_StyledBackground, True)
        customer_widget.setStyleSheet("background-color: transparent;")
        customer_layout = QVBoxLayout(customer_widget)
        customer_layout.setSpacing(2)
        customer_layout.setContentsMargins(0, 0, 0, 0)

        customer_label = QLabel("مشتری")
        customer_label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.7); font-weight: bold; background-color: transparent;")
        customer_layout.addWidget(customer_label)

        customer_select_layout = QHBoxLayout()
        customer_select_layout.setContentsMargins(0, 0, 0, 0)
        customer_select_layout.setSpacing(5)
        
        self.customer_combo = QComboBox()
        self.customer_combo.addItem("👤 انتخاب مشتری", "")
        self.customer_combo.addItem("احمد رضایی (150 امتیاز)", "ahmad")
        self.customer_combo.addItem("مریم احمدی (450 امتیاز)", "maryam")
        self.customer_combo.addItem("علی محمدی (VIP)", "ali")
        self.customer_combo.currentIndexChanged.connect(self.on_customer_changed)
        self.customer_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.4);
                border-radius: 12px;
                padding: 8px 12px;
                min-width: 135px;
                font-size: 12px;
                font-weight: 500;
            }
            QComboBox::drop-down { border: none; width: 25px; }
            QComboBox:hover { background-color: rgba(255,255,255,0.35); }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1E293B;
                border: 2px solid #8B5CF6;
                border-radius: 12px;
                padding: 6px;
                selection-background-color: #8B5CF6;
                selection-color: white;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px 14px;
                border-radius: 8px;
                margin: 2px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: rgba(139, 92, 246, 0.15);
                color: #1E293B;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #8B5CF6;
                color: white;
            }
        """)
        customer_select_layout.addWidget(self.customer_combo)

        add_customer_btn = QPushButton("+")
        add_customer_btn.setToolTip("افزودن مشتری جدید")
        add_customer_btn.setCursor(Qt.PointingHandCursor)
        add_customer_btn.clicked.connect(self.add_new_customer)
        add_customer_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.3);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.45); }
            QPushButton:pressed { background-color: rgba(255,255,255,0.55); }
        """)
        customer_select_layout.addWidget(add_customer_btn)

        customer_layout.addLayout(customer_select_layout)
        controls_layout.addWidget(customer_widget)

        # Dual mode button
        dual_btn = QPushButton("🍳")
        dual_btn.setToolTip("حالت دوپنل (آشپزخانه)")
        dual_btn.setCursor(Qt.PointingHandCursor)
        dual_btn.clicked.connect(self.toggle_dual_mode)
        dual_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF9500,
                    stop:1 #FF6B00);
                color: white;
                border: none;
                border-radius: 14px;
                padding: 12px 16px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFB347,
                    stop:1 #FF9500);
            }
            QPushButton:pressed { background-color: #E67300; }
        """)
        controls_layout.addWidget(dual_btn)

        # Settings button
        settings_btn = QPushButton("⚙️")
        settings_btn.setToolTip("تنظیمات پیشرفته")
        settings_btn.setCursor(Qt.PointingHandCursor)
        settings_btn.clicked.connect(self.show_settings)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.35);
                border-radius: 14px;
                padding: 12px 16px;
                font-size: 18px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.35); }
            QPushButton:pressed { background-color: rgba(255,255,255,0.45); }
        """)
        controls_layout.addWidget(settings_btn)

        header_layout.addLayout(controls_layout)
        products_layout.addWidget(self.header_widget)

        # Search bar
        search_widget = QWidget()
        search_widget.setAttribute(Qt.WA_StyledBackground, True)
        search_widget.setStyleSheet(f"background-color: {theme.get('bg_secondary')}; border-radius: 8px; padding: 5px;")
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 5, 10, 5)
        search_layout.setSpacing(8)

        search_label = QLabel("🔍")
        search_label.setStyleSheet(f"font-size: 18px; color: {theme.get('text_secondary')}; background-color: transparent;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو محصولات...")
        self.search_input.textChanged.connect(self.filter_products)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {theme.get('border_light')};
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                background-color: {theme.get('bg_main')};
                color: {theme.get('text_primary')};
            }}
            QLineEdit:focus {{
                border-color: {theme.get('primary')};
            }}
        """)

        clear_search_btn = QPushButton("✕")
        clear_search_btn.setToolTip("پاک کردن جستجو")
        clear_search_btn.clicked.connect(lambda: self.search_input.clear())
        clear_search_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                font-size: 16px;
                color: {theme.get('text_tertiary')};
                padding: 8px;
            }}
            QPushButton:hover {{
                color: {theme.get('error')};
                background-color: rgba(220, 38, 38, 0.1);
                border-radius: 6px;
            }}
        """)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(clear_search_btn)
        products_layout.addWidget(search_widget)

        # Category tabs
        self.category_tabs = QTabWidget()
        self.category_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {theme.get('bg_main')};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {theme.get('bg_tertiary')};
                color: {theme.get('text_secondary')};
                border: none;
                padding: 12px 20px;
                margin-right: 3px;
                border-radius: 8px 8px 0 0;
                font-size: 13px;
                font-weight: 600;
                min-width: 90px;
            }}
            QTabBar::tab:selected {{
                background-color: {theme.get('bg_main')};
                color: {theme.get('primary')};
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background-color: {theme.get('bg_hover')};
                color: {theme.get('text_primary')};
            }}
        """)
        products_layout.addWidget(self.category_tabs, 1)

        # Quick actions
        self.setup_quick_actions(products_layout)

        parent_layout.addWidget(products_widget, 2)

    def setup_quick_actions(self, parent_layout):
        """Setup quick action buttons"""
        theme = self.theme_manager.current_theme
        
        actions_widget = QWidget()
        actions_widget.setAttribute(Qt.WA_StyledBackground, True)
        actions_widget.setStyleSheet(f"background-color: {theme.get('bg_secondary')}; border-radius: 8px;")
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(10, 8, 10, 8)
        actions_layout.setSpacing(8)

        buttons = [
            ("⭐ محبوب‌ترین", theme.get('accent'), self.show_popular_items),
            ("🕐 اخیر", "#8B5CF6", self.show_recent_orders),
            ("👤 مشتری", theme.get('info'), self.show_customer_info),
        ]

        for text, color, callback in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 14px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {color}DD; }}
                QPushButton:pressed {{ background-color: {color}BB; }}
            """)
            actions_layout.addWidget(btn)

        actions_layout.addStretch()

        shortcuts_label = QLabel("⌨️ F12: تسویه • Ctrl+F: جستجو • F1-F9: میزها")
        shortcuts_label.setStyleSheet(f"font-size: 10px; color: {theme.get('text_tertiary')}; background-color: transparent;")
        actions_layout.addWidget(shortcuts_label)

        parent_layout.addWidget(actions_widget)

    def setup_cart_section(self, parent_layout):
        """Setup enhanced cart/order section"""
        theme = self.theme_manager.current_theme
        
        cart_widget = QWidget()
        cart_widget.setProperty("class", "cart-section")
        cart_widget.setAttribute(Qt.WA_StyledBackground, True)
        cart_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_card')};
                border: 1px solid {theme.get('border_light')};
                border-radius: 24px;
            }}
        """)
        cart_layout = QVBoxLayout(cart_widget)
        cart_layout.setContentsMargins(15, 15, 15, 15)
        cart_layout.setSpacing(12)

        # Header
        header_layout = QHBoxLayout()
        cart_title = QLabel("🛒 سفارش جاری")
        cart_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {theme.get('text_primary')};")

        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"font-size: 12px; color: {theme.get('text_secondary')};")
        self.update_time()

        header_layout.addWidget(cart_title)
        header_layout.addStretch()
        header_layout.addWidget(self.time_label)
        cart_layout.addLayout(header_layout)

        # Stats
        self.stats_label = QLabel("📊 ۰ سفارش • ۰ تومان")
        self.stats_label.setStyleSheet(f"font-size: 12px; color: {theme.get('text_secondary')};")
        cart_layout.addWidget(self.stats_label)

        # Order list
        self.order_list = QListWidget()
        self.order_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {theme.get('border_light')};
                border-radius: 8px;
                background-color: {theme.get('bg_input')};
                padding: 5px;
            }}
            QListWidget::item {{
                border: none;
                padding: 3px 0;
            }}
            QListWidget::item:hover {{
                background-color: {theme.get('bg_hover')};
            }}
        """)
        cart_layout.addWidget(self.order_list, 1)

        # Discount section
        discount_layout = QHBoxLayout()
        discount_layout.setSpacing(8)

        discount_label = QLabel("تخفیف:")
        discount_label.setStyleSheet(f"font-size: 13px; color: {theme.get('text_secondary')};")

        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText("مبلغ")
        self.discount_input.setMaximumWidth(80)
        self.discount_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {theme.get('border_light')};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                background-color: {theme.get('bg_input')};
            }}
            QLineEdit:focus {{ border-color: {theme.get('accent')}; }}
        """)

        apply_discount_btn = QPushButton("✅ اعمال")
        apply_discount_btn.clicked.connect(self.apply_discount)
        apply_discount_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.get('accent')};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {theme.get('accent_dark')}; }}
        """)

        discount_layout.addWidget(discount_label)
        discount_layout.addWidget(self.discount_input)
        discount_layout.addWidget(apply_discount_btn)
        discount_layout.addStretch()
        cart_layout.addLayout(discount_layout)

        # Totals
        totals_widget = QWidget()
        totals_widget.setAttribute(Qt.WA_StyledBackground, True)
        totals_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme.get('bg_secondary')},
                    stop:1 {theme.get('bg_tertiary')});
                border: 1px solid {theme.get('border_light')};
                border-radius: 16px;
                padding: 12px;
            }}
        """)
        totals_layout = QVBoxLayout(totals_widget)
        totals_layout.setSpacing(6)
        totals_layout.setContentsMargins(12, 10, 12, 10)

        self.subtotal_label = QLabel("جمع جزء: 0 تومان")
        self.subtotal_label.setStyleSheet(f"color: {theme.get('text_secondary')}; font-size: 13px;")

        self.discount_label = QLabel("تخفیف: 0 تومان")
        self.discount_label.setStyleSheet(f"color: {theme.get('warning')}; font-size: 13px;")

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {theme.get('border_light')};")

        self.total_label = QLabel("مجموع: 0 تومان")
        self.total_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {theme.get('secondary')};")

        totals_layout.addWidget(self.subtotal_label)
        totals_layout.addWidget(self.discount_label)
        totals_layout.addWidget(separator)
        totals_layout.addWidget(self.total_label)

        cart_layout.addWidget(totals_widget)

        # Buttons
        self.checkout_btn = QPushButton("💰 تسویه حساب")
        self.checkout_btn.setProperty("class", "action-btn")
        self.checkout_btn.setCursor(Qt.PointingHandCursor)
        self.checkout_btn.clicked.connect(self.checkout_order)
        self.checkout_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme.get('secondary')},
                    stop:1 {theme.get('secondary_light')});
                color: white;
                border: none;
                border-radius: 16px;
                padding: 18px;
                font-size: 17px;
                font-weight: bold;
            }}
            QPushButton:hover {{ 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme.get('secondary_dark')},
                    stop:1 {theme.get('secondary')});
            }}
        """)
        cart_layout.addWidget(self.checkout_btn)

        extra_buttons_layout = QHBoxLayout()
        extra_buttons_layout.setSpacing(8)

        self.print_receipt_btn = QPushButton("🖨️ چاپ قبض")
        self.print_receipt_btn.setCursor(Qt.PointingHandCursor)
        self.print_receipt_btn.clicked.connect(self.print_current_receipt)
        self.print_receipt_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme.get('text_tertiary')};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {theme.get('text_secondary')}; }}
        """)
        extra_buttons_layout.addWidget(self.print_receipt_btn)

        self.clear_btn = QPushButton("🗑️ پاک کردن")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_order)
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme.get('error')},
                    stop:1 #F87171);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{ 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #B91C1C,
                    stop:1 {theme.get('error')});
            }}
        """)
        extra_buttons_layout.addWidget(self.clear_btn)

        cart_layout.addLayout(extra_buttons_layout)

        parent_layout.addWidget(cart_widget, 1)

    def setup_timers(self):
        """Setup timers for real-time updates"""
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(5000)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        from PySide6.QtGui import QShortcut, QKeySequence

        QShortcut(QKeySequence("F12"), self).activated.connect(self.checkout_order)
        QShortcut(QKeySequence("Ctrl+Delete"), self).activated.connect(self.clear_order)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(lambda: self.search_input.setFocus())
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.clear_order)
        QShortcut(QKeySequence("Ctrl+P"), self).activated.connect(self.print_current_receipt)

        for i in range(1, 10):
            QShortcut(QKeySequence(f"F{i}"), self).activated.connect(lambda t=i: self.quick_table_select(t))

    def load_menu_data(self):
        """Load menu data and create category tabs"""
        self.category_tabs.clear()
        categories = self.menu_service.get_categories()

        # "همه" tab
        all_tab = self.create_category_tab("همه")
        self.category_tabs.addTab(all_tab, "🍽️ همه")

        for category in sorted(categories):
            tab = self.create_category_tab(category)
            self.category_tabs.addTab(tab, f"📂 {category}")

    def create_category_tab(self, category):
        """Create a category tab with products"""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(5, 5, 5, 5)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        products_container = QWidget()
        grid = QGridLayout(products_container)
        grid.setSpacing(12)
        grid.setContentsMargins(5, 5, 5, 5)

        if category == "همه":
            products = self.menu_service.get_active_products()
        else:
            products = self.menu_service.get_products_by_category(category)

        row, col = 0, 0
        max_cols = 4  # More columns for better use of space

        for product in products:
            product_card = self.create_product_card(product)
            grid.addWidget(product_card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        scroll_area.setWidget(products_container)
        tab_layout.addWidget(scroll_area)

        return tab

    def create_product_card(self, product):
        """Create an enhanced product card - Modern & Soft"""
        theme = self.theme_manager.current_theme
        
        card = QWidget()
        card.setMinimumSize(150, 140)
        card.setMaximumSize(180, 165)
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_card')};
                border: 1px solid {theme.get('border_light')};
                border-radius: 18px;
            }}
            QWidget:hover {{
                border: 2px solid {theme.get('primary')};
                background-color: {theme.get('bg_hover')};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Name
        name = product.name[:16] + "..." if len(product.name) > 16 else product.name
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {theme.get('text_primary')}; background-color: transparent;")
        layout.addWidget(name_label)

        # Category - Pill style
        cat = product.category[:12] + "..." if len(product.category) > 12 else product.category
        category_label = QLabel(f"📂 {cat}")
        category_label.setAlignment(Qt.AlignCenter)
        category_label.setStyleSheet(f"""
            font-size: 10px; 
            color: {theme.get('text_secondary')}; 
            background-color: {theme.get('bg_tertiary')}; 
            padding: 4px 10px; 
            border-radius: 10px;
        """)
        layout.addWidget(category_label)

        # Price - Gradient background
        price_label = QLabel(f"💰 {product.price:,}")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet(f"""
            font-size: 14px; 
            font-weight: bold; 
            color: {theme.get('accent')}; 
            background-color: transparent;
            padding: 2px;
        """)
        layout.addWidget(price_label)

        # Add button - Modern gradient
        add_btn = QPushButton("➕ افزودن")
        add_btn.setToolTip(f"افزودن {product.name} به سفارش")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(lambda: self.add_product_to_order(product.id))
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme.get('secondary')},
                    stop:1 {theme.get('secondary_light')});
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {theme.get('secondary_dark')},
                    stop:1 {theme.get('secondary')});
            }}
            QPushButton:pressed {{ 
                background-color: {theme.get('secondary_dark')}; 
            }}
        """)
        layout.addWidget(add_btn)

        return card

    # ========== Event Handlers ==========

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
            
            if table_number is None:
                self.table_indicator.setStyleSheet("""
                    QLabel {
                        font-size: 16px; font-weight: bold; color: #FFA500;
                        background-color: rgba(255,165,0,0.15);
                        padding: 8px 16px; border-radius: 20px;
                        border: 2px solid rgba(255,165,0,0.4);
                    }
                """)
            else:
                self.table_indicator.setStyleSheet("""
                    QLabel {
                        font-size: 16px; font-weight: bold; color: #FFD700;
                        background-color: rgba(255,255,255,0.15);
                        padding: 8px 16px; border-radius: 20px;
                        border: 2px solid rgba(255,255,255,0.3);
                    }
                """)

            self.refresh_cart()
        except ValueError as e:
            QMessageBox.warning(self, "خطا", str(e))

    def on_customer_changed(self):
        """Handle customer selection change"""
        customer_data = self.customer_combo.currentData()
        if customer_data:
            customer_name = self.customer_combo.currentText().split(" (")[0]
            self.show_notification("مشتری انتخاب شد", f"خوش آمدید {customer_name}!", "👤")
            self.current_customer = customer_data
        else:
            self.current_customer = None

    def change_theme(self):
        """Change application theme"""
        theme_index = self.theme_combo.currentIndex()
        theme_names = ["modern_blue", "dark", "warm_orange", "coffee_brown"]
        
        if 0 <= theme_index < len(theme_names):
            self.theme_manager.set_theme_by_name(theme_names[theme_index])
            self.show_notification("تم تغییر یافت", 
                f"تم به '{self.theme_combo.currentText()}' تغییر یافت! ✨", "🎨")

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
        theme = self.theme_manager.current_theme
        self.order_list.clear()

        for item in self.order_service.get_items():
            item_widget = QWidget()
            item_widget.setAttribute(Qt.WA_StyledBackground, True)
            item_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme.get('bg_main')};
                    border: 1px solid {theme.get('border_light')};
                    border-radius: 10px;
                }}
            """)
            item_widget.setMinimumHeight(50)
            
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(10, 8, 10, 8)
            item_layout.setSpacing(10)

            # Product name
            name_label = QLabel(item.name)
            name_label.setStyleSheet(f"""
                font-weight: bold; 
                font-size: 13px; 
                color: {theme.get('text_primary')};
                background: transparent;
                border: none;
                min-width: 80px;
            """)
            item_layout.addWidget(name_label, 1)

            # Quantity display with styled box
            qty_container = QWidget()
            qty_container.setAttribute(Qt.WA_StyledBackground, True)
            qty_container.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme.get('bg_tertiary')};
                    border-radius: 8px;
                    border: none;
                }}
            """)
            qty_layout = QHBoxLayout(qty_container)
            qty_layout.setContentsMargins(6, 4, 6, 4)
            qty_layout.setSpacing(4)
            
            # Minus button
            minus_btn = QPushButton("−")
            minus_btn.setFixedSize(28, 28)
            minus_btn.setCursor(Qt.PointingHandCursor)
            minus_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.get('primary')};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {theme.get('primary_light')}; }}
            """)
            minus_btn.clicked.connect(lambda c, n=item.name, q=item.quantity: self.update_item_quantity(n, max(1, q-1)))
            qty_layout.addWidget(minus_btn)
            
            # Quantity label
            qty_label = QLabel(f"{item.quantity}")
            qty_label.setAlignment(Qt.AlignCenter)
            qty_label.setFixedWidth(35)
            qty_label.setStyleSheet(f"""
                font-size: 15px; 
                font-weight: bold; 
                color: {theme.get('text_primary')};
                background: transparent;
                border: none;
            """)
            qty_layout.addWidget(qty_label)
            
            # Plus button
            plus_btn = QPushButton("+")
            plus_btn.setFixedSize(28, 28)
            plus_btn.setCursor(Qt.PointingHandCursor)
            plus_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.get('secondary')};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {theme.get('secondary_dark')}; }}
            """)
            plus_btn.clicked.connect(lambda c, n=item.name, q=item.quantity: self.update_item_quantity(n, q+1))
            qty_layout.addWidget(plus_btn)
            
            item_layout.addWidget(qty_container)

            # Price label
            price_label = QLabel(f"{item.total_price().amount:,}")
            price_label.setStyleSheet(f"""
                color: {theme.get('accent')}; 
                font-weight: bold; 
                font-size: 13px;
                background: transparent;
                border: none;
                min-width: 70px;
            """)
            price_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            item_layout.addWidget(price_label)

            # Remove button
            remove_btn = QPushButton("✕")
            remove_btn.setFixedSize(32, 32)
            remove_btn.setCursor(Qt.PointingHandCursor)
            remove_btn.clicked.connect(lambda c, n=item.name: self.remove_item(n))
            remove_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.get('error')};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: #DC2626; }}
            """)
            item_layout.addWidget(remove_btn)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.order_list.addItem(list_item)
            self.order_list.setItemWidget(list_item, item_widget)

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
                QMessageBox.information(self, "سفارش ثبت شد",
                    f"سفارش با شماره {order_id} با موفقیت ثبت شد!\n\nمجموع: {total.amount:,} تومان")
                self.show_notification("سفارش تسویه شد", f"مبلغ: {total.amount:,} تومان", "💰")
                
                if self.dual_mode and self.kitchen_display:
                    self.kitchen_display.update_orders()
                
                self.refresh_cart()
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در ثبت سفارش: {str(e)}")

    def clear_order(self):
        """Clear current order"""
        if self.order_service.get_items():
            reply = QMessageBox.question(self, "تأیید پاک کردن",
                "آیا مطمئن هستید که می‌خواهید سفارش را پاک کنید؟",
                QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                current_table = self.order_service.get_table_number()
                self.order_service = OrderService()
                if current_table:
                    self.order_service.set_table(current_table)
                self.refresh_cart()

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
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در اعمال تخفیف: {str(e)}")

    def update_time(self):
        """Update the time display"""
        self.time_label.setText(f"📅 {datetime.now().strftime('%Y/%m/%d')} 🕐 {datetime.now().strftime('%H:%M:%S')}")

    def update_stats(self):
        """Update daily statistics display"""
        try:
            from application.report_service import ReportService
            report_service = ReportService()
            today_stats = report_service.get_daily_sales()
            self.stats_label.setText(f"📊 {today_stats['orders_count']} سفارش • {today_stats['net_sales'].amount:,} تومان")
        except:
            self.stats_label.setText(f"📊 {len(self.order_service.get_items())} آیتم")

    def filter_products(self):
        """Filter products based on search text"""
        search_text = self.search_input.text().lower().strip()

        for tab_index in range(self.category_tabs.count()):
            tab_widget = self.category_tabs.widget(tab_index)
            if tab_widget:
                scroll_area = tab_widget.findChild(QScrollArea)
                if scroll_area and scroll_area.widget():
                    for child in scroll_area.widget().findChildren(QWidget):
                        if child.parent() == scroll_area.widget():
                            labels = child.findChildren(QLabel)
                            visible = not search_text
                            for label in labels:
                                if search_text in label.text().lower():
                                    visible = True
                                    break
                            child.setVisible(visible)

    # ========== Dual Mode ==========

    def toggle_dual_mode(self):
        """Toggle between single and dual monitor mode"""
        self.dual_mode = not self.dual_mode

        if self.dual_mode:
            self.kitchen_display = KitchenDisplayWidget(self.order_service)
            self.kitchen_display.show()
            
            if len(self.screens()) > 1:
                second_screen = self.screens()[1].availableGeometry()
                self.kitchen_display.move(second_screen.x(), second_screen.y())
                self.kitchen_display.resize(second_screen.width(), second_screen.height())
            else:
                self.kitchen_display.move(self.x() + self.width() + 10, self.y())
            
            self.resize(1000, 900)
            self.show_notification("حالت دوپنل فعال شد", "نمایش آشپزخانه باز شده است", "🍳")
        else:
            if self.kitchen_display:
                self.kitchen_display.close()
                self.kitchen_display = None
            self.resize(1400, 900)
            self.show_notification("حالت تک‌پنل فعال شد", "به حالت عادی بازگشتیم", "💻")

    # ========== Dialogs ==========

    def add_new_customer(self):
        """Add new customer"""
        from ui.add_customer_dialog import AddCustomerDialog
        dialog = AddCustomerDialog(self)
        if dialog.exec():
            self.customer_combo.clear()
            self.customer_combo.addItem("👤 انتخاب مشتری", "")
            self.customer_combo.addItem("احمد رضایی (150 امتیاز)", "ahmad")
            self.customer_combo.addItem("مریم احمدی (450 امتیاز)", "maryam")
            self.customer_combo.addItem("علی محمدی (VIP)", "ali")
            new_customer_name = dialog.name_input.text()
            self.customer_combo.addItem(f"{new_customer_name} (50 امتیاز)", "new")
            self.show_notification("مشتری اضافه شد", f"{new_customer_name} به باشگاه مشتریان اضافه شد!", "✅")

    def show_settings(self):
        """Show advanced settings dialog"""
        from ui.advanced_settings_dialog import AdvancedSettingsDialog
        dialog = AdvancedSettingsDialog(self)
        dialog.exec()

    def show_popular_items(self):
        """Show popular items tab"""
        self.category_tabs.setCurrentIndex(0)
        self.show_notification("محبوب‌ترین محصولات", "تب همه محصولات نمایش داده شد", "⭐")

    def show_recent_orders(self):
        """Show recent orders dialog"""
        try:
            from application.report_service import ReportService
            today_report = ReportService().get_daily_sales()
            popular_products = today_report.get('top_products', [])

            if popular_products:
                message = "محبوب‌ترین محصولات امروز:\n" + "\n".join([
                    f"• {p['name']}: {p['quantity']} عدد" for p in popular_products[:5]])
            else:
                message = "هنوز سفارشی ثبت نشده است"

            QMessageBox.information(self, "سفارشات اخیر", message)
        except:
            QMessageBox.information(self, "سفارشات اخیر", "امکان نمایش آمار وجود ندارد")

    def show_customer_info(self):
        """Show customer information dialog"""
        current_table = self.order_service.get_table_number()
        items_count = len(self.order_service.get_items())
        total_amount = self.order_service.get_total_price().amount

        QMessageBox.information(self, "اطلاعات مشتری", f"""
📊 اطلاعات سفارش جاری:

میز: {"بیرون بر" if current_table is None else f"میز {current_table}"}
تعداد آیتم‌ها: {items_count}
مجموع مبلغ: {total_amount:,} تومان
زمان: {datetime.now().strftime("%H:%M:%S")}
        """.strip())

    def print_current_receipt(self):
        """Print receipt for current order"""
        if not self.order_service.get_items():
            QMessageBox.warning(self, "خطا", "سفارش خالی نمی‌تواند چاپ شود")
            return

        try:
            from infrastructure.printer.receipt_printer import ReceiptPrinter
            printer = ReceiptPrinter()

            temp_order = type('TempOrder', (), {})()
            temp_order.items = self.order_service.get_items()
            temp_order.status = type('Status', (), {'value': 'CLOSED'})()
            temp_order.discount = self.order_service.get_discount()
            temp_order.total_price = lambda: self.order_service.get_total_price()
            temp_order.table_number = self.order_service.get_table_number()

            printer.print_receipt(temp_order, 0)
            QMessageBox.information(self, "موفق", "فاکتور به پرینتر ارسال شد!")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در چاپ فاکتور: {str(e)}")

    def quick_table_select(self, table_number):
        """Quick table selection via keyboard shortcuts"""
        if 1 <= table_number <= 20:
            self.table_combo.setCurrentIndex(table_number - 1)

    def show_notification(self, title, message, icon="ℹ️"):
        """Show a notification toast"""
        theme = self.theme_manager.current_theme
        
        notification = QWidget(self)
        notification.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        notification.setAttribute(Qt.WA_StyledBackground, True)
        notification.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_card')};
                color: {theme.get('text_primary')};
                border-radius: 16px;
                border: 1px solid {theme.get('border_light')};
            }}
        """)

        layout = QHBoxLayout(notification)
        layout.setContentsMargins(15, 12, 15, 12)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px; background-color: transparent;")

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {theme.get('text_primary')}; background-color: transparent;")
        message_label = QLabel(message)
        message_label.setStyleSheet(f"font-size: 12px; color: {theme.get('text_secondary')}; background-color: transparent;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)

        layout.addWidget(icon_label)
        layout.addLayout(text_layout)

        notification.adjustSize()
        notification.move(self.width() - notification.width() - 20,
                         self.height() - notification.height() - 20)
        notification.show()

        QTimer.singleShot(3000, notification.hide)
