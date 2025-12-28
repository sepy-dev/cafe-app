#main_window
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt

from ui.order_view import OrderView
from ui.menu_view import MenuView
from ui.reports_view import ReportsView
from ui.menu_management_dialog import MenuManagementDialog
from ui.backup_dialog import BackupDialog
from ui.printer_settings_dialog import PrinterSettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cafe Order System")
        self.resize(1100, 700)

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QHBoxLayout(container)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)

        btn_orders = QPushButton("سفارشات")
        btn_menu = QPushButton("منو")
        btn_menu_management = QPushButton("مدیریت منو")
        btn_reports = QPushButton("گزارشات")
        btn_backup = QPushButton("پشتیبان")
        btn_settings = QPushButton("⚙️ تنظیمات")

        sidebar.addWidget(btn_orders)
        sidebar.addWidget(btn_menu)
        sidebar.addWidget(btn_menu_management)
        sidebar.addWidget(btn_reports)
        sidebar.addWidget(btn_backup)
        sidebar.addWidget(btn_settings)

        # Pages
        self.pages = QStackedWidget()
        self.order_view = OrderView()
        self.menu_view = MenuView()
        self.reports_view = ReportsView()

        self.pages.addWidget(self.order_view)
        self.pages.addWidget(self.menu_view)
        self.pages.addWidget(self.reports_view)

        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.pages, 5)

        # Navigation
        btn_orders.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        btn_menu.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        btn_menu_management.clicked.connect(self.show_menu_management)
        btn_reports.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        btn_backup.clicked.connect(self.show_backup_dialog)
        btn_settings.clicked.connect(self.show_settings)
    # بعد از ساخت view ها
        self.menu_view.product_selected.connect(
        self.on_product_selected
        )   

    def on_product_selected(self, product_id: int):
        product = self.menu_view.menu_service.get_product_by_id(product_id)

        self.order_view.order_service.add_item(
            name=product.name,
            price=product.price,
            quantity=1
        )
        self.order_view.refresh_ui()

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
