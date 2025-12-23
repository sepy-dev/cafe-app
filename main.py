import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
