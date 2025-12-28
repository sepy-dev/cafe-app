#main_window
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

from ui.order_view import OrderView
from ui.menu_view import MenuView
from ui.reports_view import ReportsView
from ui.menu_management_dialog import MenuManagementDialog
from ui.backup_dialog import BackupDialog
from ui.printer_settings_dialog import PrinterSettingsDialog
from ui.styles import ModernStyles, FontManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍽️ سیستم مدیریت کافه - مدرن")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 600)

        # Apply modern styling
        self.setStyleSheet(ModernStyles.get_main_style())
        self.setFont(FontManager.get_main_font())

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Modern Sidebar
        self.setup_sidebar(main_layout)

        # Main Content Area
        self.setup_main_content(main_layout)

        # Connect signals
        self.setup_connections()

    def setup_sidebar(self, parent_layout):
        """Setup modern sidebar"""
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setFixedWidth(250)
        sidebar_widget.setStyleSheet("""
            QWidget#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2C3E50, stop:1 #34495E);
                border-right: 1px solid #BDC3C7;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(8)

        # Logo/Title
        logo_label = QLabel("☕ مدیریت کافه")
        logo_label.setObjectName("logo")
        logo_label.setStyleSheet("""
            QLabel#logo {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                text-align: center;
                margin-bottom: 20px;
            }
        """)
        sidebar_layout.addWidget(logo_label)

        # Navigation Buttons
        self.nav_buttons = {}

        nav_items = [
            ("btn_orders", "📋 سفارشات", 0),
            ("btn_menu", "🍽️ منو", 1),
            ("btn_reports", "📊 گزارشات", 2),
        ]

        for btn_id, text, index in nav_items:
            btn = QPushButton(text)
            btn.setObjectName(btn_id)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #BDC3C7;
                    text-align: left;
                    padding: 15px 20px;
                    margin: 2px 10px;
                    border-radius: 10px;
                    font-size: 13px;
                    font-weight: 500;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.1);
                    color: white;
                }
                QPushButton:checked {
                    background-color: #3498DB;
                    color: white;
                    font-weight: bold;
                }
            """)
            btn.clicked.connect(lambda checked, idx=index: self.switch_page(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[btn_id] = btn

        # Spacer
        sidebar_layout.addStretch()

        # Management Buttons
        management_layout = QVBoxLayout()
        management_layout.setContentsMargins(10, 10, 10, 20)
        management_layout.setSpacing(5)

        management_title = QLabel("⚙️ مدیریت")
        management_title.setStyleSheet("color: #BDC3C7; font-weight: bold; padding: 10px;")
        management_layout.addWidget(management_title)

        self.btn_menu_management = QPushButton("🍽️ مدیریت منو")
        self.btn_menu_management.clicked.connect(self.show_menu_management)
        self.btn_menu_management.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #BDC3C7;
                text-align: left;
                padding: 10px 15px;
                margin: 2px 5px;
                border-radius: 8px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
                color: white;
            }
        """)
        management_layout.addWidget(self.btn_menu_management)

        self.btn_backup = QPushButton("💾 پشتیبان")
        self.btn_backup.clicked.connect(self.show_backup_dialog)
        self.btn_backup.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #BDC3C7;
                text-align: left;
                padding: 10px 15px;
                margin: 2px 5px;
                border-radius: 8px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
                color: white;
            }
        """)
        management_layout.addWidget(self.btn_backup)

        self.btn_settings = QPushButton("⚙️ تنظیمات")
        self.btn_settings.clicked.connect(self.show_settings)
        self.btn_settings.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #BDC3C7;
                text-align: left;
                padding: 10px 15px;
                margin: 2px 5px;
                border-radius: 8px;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
                color: white;
            }
        """)
        management_layout.addWidget(self.btn_settings)

        sidebar_layout.addLayout(management_layout)

        parent_layout.addWidget(sidebar_widget)

    def setup_main_content(self, parent_layout):
        """Setup main content area"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        self.page_title = QLabel("سفارشات")
        self.page_title.setProperty("class", "title")
        header_layout.addWidget(self.page_title)

        header_layout.addStretch()

        # Current table indicator
        self.table_indicator = QLabel("میز: انتخاب نشده")
        self.table_indicator.setStyleSheet("""
            QLabel {
                background-color: #ECF0F1;
                color: #2C3E50;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(self.table_indicator)

        content_layout.addLayout(header_layout)

        # Pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("""
            QStackedWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
        """)

        self.order_view = OrderView()
        self.menu_view = MenuView()
        self.reports_view = ReportsView()

        self.pages.addWidget(self.order_view)
        self.pages.addWidget(self.menu_view)
        self.pages.addWidget(self.reports_view)

        content_layout.addWidget(self.pages)

        parent_layout.addWidget(content_widget, 1)

    def setup_connections(self):
        """Setup signal connections"""
        # Menu product selection
        self.menu_view.product_selected.connect(self.on_product_selected)

        # Set initial page
        self.switch_page(0)

    def switch_page(self, index):
        """Switch to selected page"""
        self.pages.setCurrentIndex(index)

        # Update navigation buttons
        page_titles = ["سفارشات", "منو", "گزارشات"]
        self.page_title.setText(page_titles[index])

        # Update button states
        for btn_id, btn in self.nav_buttons.items():
            btn.setChecked(False)
        if index < len(self.nav_buttons):
            list(self.nav_buttons.values())[index].setChecked(True)   

    def on_product_selected(self, product_id: int):
        try:
            product = self.menu_view.menu_service.get_product_by_id(product_id)

            self.order_view.order_service.add_item(
                name=product.name,
                price=product.price,
                quantity=1
            )
            self.order_view.refresh_ui()
            self.update_table_indicator()
        except ValueError as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "خطا", f"لطفاً ابتدا میز را انتخاب کنید: {str(e)}")

    def show_menu_management(self):
        """نمایش دیالوگ مدیریت منو"""
        dialog = MenuManagementDialog(self)
        dialog.exec()

        # بروزرسانی منو بعد از تغییرات
        self.menu_view.load_menu()

    def show_backup_dialog(self):
        """نمایش دیالوگ مدیریت پشتیبان"""
        dialog = BackupDialog(self)
        dialog.exec()

    def show_settings(self):
        """نمایش دیالوگ تنظیمات"""
        dialog = PrinterSettingsDialog(self)
        dialog.exec()

    def update_table_indicator(self):
        """Update table indicator"""
        table_num = self.order_view.order_service.get_table_number()
        if table_num and table_num != 0:
            self.table_indicator.setText(f"میز {table_num}")
            self.table_indicator.setStyleSheet("""
                QLabel {
                    background-color: #27AE60;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                }
            """)
        else:
            self.table_indicator.setText("بیرون بر")
            self.table_indicator.setStyleSheet("""
                QLabel {
                    background-color: #E74C3C;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                }
            """)
