from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReportsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("گزارشات فروش")
        title.setStyleSheet("font-size:18px; font-weight:bold;")

        placeholder = QLabel("گزارش روزانه / ماهانه اینجا نمایش داده می‌شود")

        layout.addWidget(title)
        layout.addWidget(placeholder)
