from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
)


class MenuView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("مدیریت منو")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        self.menu_list = QListWidget()
        self.btn_add = QPushButton("افزودن آیتم")
        self.btn_edit = QPushButton("ویرایش")
        self.btn_delete = QPushButton("حذف")

        layout.addWidget(title)
        layout.addWidget(self.menu_list)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)
