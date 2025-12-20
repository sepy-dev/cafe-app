from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Signal


class KeypadWidget(QWidget):
    value_entered = Signal(int)

    def __init__(self):
        super().__init__()

        self.current_value = ""

        layout = QGridLayout(self)

        buttons = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0", "C", "OK"
        ]

        positions = [(i, j) for i in range(4) for j in range(3)]

        for pos, text in zip(positions, buttons):
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, t=text: self._on_click(t))
            layout.addWidget(btn, *pos)

    def _on_click(self, text: str):
        if text == "C":
            self.current_value = ""
        elif text == "OK":
            if self.current_value:
                self.value_entered.emit(int(self.current_value))
                self.current_value = ""
        else:
            self.current_value += text
