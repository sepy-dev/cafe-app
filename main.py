import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import os

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# راه‌اندازی دیتابیس
from infrastructure.database.session import init_db
init_db()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
