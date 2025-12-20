import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
