#menu_view
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Signal

from application.menu_service import MenuService
#kd

class MenuView(QWidget):
    product_selected = Signal(int)  # product_id

    def __init__(self):
        super().__init__()

        self.menu_service = MenuService()

        layout = QVBoxLayout(self)

        title = QLabel("منو")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        self.menu_list = QListWidget()
        layout.addWidget(title)
        layout.addWidget(self.menu_list)

        self.load_menu()
        self.menu_list.itemClicked.connect(self.on_item_clicked)

    def load_menu(self):
        self.menu_list.clear()

        for product in self.menu_service.get_active_products():
            item = QListWidgetItem(
                f"{product.name} - {product.price} تومان"
            )
            item.setData(1, product.id)
            self.menu_list.addItem(item)

    def on_item_clicked(self, item: QListWidgetItem):
        product_id = item.data(1)
        self.product_selected.emit(product_id)
