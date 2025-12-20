from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt

from ui.order_view import OrderView
from ui.menu_view import MenuView
from ui.reports_view import ReportsView


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
        btn_reports = QPushButton("گزارشات")

        sidebar.addWidget(btn_orders)
        sidebar.addWidget(btn_menu)
        sidebar.addWidget(btn_reports)

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
        btn_reports.clicked.connect(lambda: self.pages.setCurrentIndex(2))
