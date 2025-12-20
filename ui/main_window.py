#main_window
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
