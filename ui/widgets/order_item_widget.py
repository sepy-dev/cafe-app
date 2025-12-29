from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpinBox
from PySide6.QtCore import Signal, Qt
from ui.styles import ThemeManager


class OrderItemWidget(QWidget):
    """Modern order item widget with smooth design"""
    quantity_changed = Signal(str, int)  # name, new_quantity

    def __init__(self, name: str, qty: int, price: int):
        super().__init__()
        self.setProperty("class", "order-item")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        theme = ThemeManager.instance().current_theme

        # Main widget style - Soft card design
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_main')};
                border: 1px solid {theme.get('border_light')};
                border-radius: 14px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(12)

        # نام محصول - با آیکون زیبا
        name_container = QWidget()
        name_container.setAttribute(Qt.WA_StyledBackground, True)
        name_container.setStyleSheet("background: transparent; border: none;")
        name_layout = QVBoxLayout(name_container)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(2)
        
        self.lbl_name = QLabel(f"🍽️ {name}")
        self.lbl_name.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                font-size: 14px;
                color: {theme.get('primary')};
                background: transparent;
                border: none;
                min-width: 140px;
            }}
        """)
        name_layout.addWidget(self.lbl_name)
        layout.addWidget(name_container)

        # کنترل تعداد - طراحی مدرن
        qty_widget = QWidget()
        qty_widget.setAttribute(Qt.WA_StyledBackground, True)
        qty_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('bg_tertiary')};
                border-radius: 10px;
                border: none;
                padding: 4px;
            }}
        """)
        qty_layout = QVBoxLayout(qty_widget)
        qty_layout.setContentsMargins(8, 6, 8, 6)
        qty_layout.setSpacing(2)

        qty_label = QLabel("تعداد")
        qty_label.setStyleSheet(f"""
            font-size: 9px; 
            color: {theme.get('text_secondary')}; 
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        qty_label.setAlignment(Qt.AlignCenter)
        qty_layout.addWidget(qty_label)

        self.qty_spin = QSpinBox()
        self.qty_spin.setMinimum(1)
        self.qty_spin.setMaximum(99)
        self.qty_spin.setValue(qty)
        self.qty_spin.setMaximumWidth(70)
        self.qty_spin.setStyleSheet(f"""
            QSpinBox {{
                border: 2px solid {theme.get('border_light')};
                border-radius: 8px;
                padding: 4px 8px;
                background-color: {theme.get('bg_input')};
                color: {theme.get('text_primary')};
                font-size: 13px;
                font-weight: bold;
            }}
            QSpinBox:focus {{
                border-color: {theme.get('primary')};
            }}
            QSpinBox::up-button {{
                border: none;
                background-color: {theme.get('bg_hover')};
                width: 18px;
                border-top-right-radius: 6px;
            }}
            QSpinBox::down-button {{
                border: none;
                background-color: {theme.get('bg_hover')};
                width: 18px;
                border-bottom-right-radius: 6px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {theme.get('primary_alpha')};
            }}
        """)
        self.qty_spin.valueChanged.connect(self.on_quantity_changed)
        qty_layout.addWidget(self.qty_spin)

        layout.addWidget(qty_widget)

        # قیمت واحد - با پس‌زمینه نارنجی
        unit_price = price // qty
        unit_widget = QWidget()
        unit_widget.setAttribute(Qt.WA_StyledBackground, True)
        unit_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('accent')}20;
                border-radius: 10px;
                border: none;
            }}
        """)
        unit_layout = QVBoxLayout(unit_widget)
        unit_layout.setContentsMargins(10, 6, 10, 6)
        unit_layout.setSpacing(2)

        unit_label = QLabel("قیمت واحد")
        unit_label.setStyleSheet(f"""
            font-size: 9px; 
            color: {theme.get('text_secondary')}; 
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_layout.addWidget(unit_label)

        self.lbl_unit_price = QLabel(f"{unit_price:,} تومان")
        self.lbl_unit_price.setStyleSheet(f"""
            QLabel {{
                color: {theme.get('accent')};
                font-weight: bold;
                font-size: 12px;
                background: transparent;
                border: none;
            }}
        """)
        self.lbl_unit_price.setAlignment(Qt.AlignCenter)
        unit_layout.addWidget(self.lbl_unit_price)

        layout.addWidget(unit_widget)

        # قیمت کل - با پس‌زمینه سبز
        total_widget = QWidget()
        total_widget.setAttribute(Qt.WA_StyledBackground, True)
        total_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {theme.get('secondary')}20;
                border-radius: 10px;
                border: none;
            }}
        """)
        total_layout = QVBoxLayout(total_widget)
        total_layout.setContentsMargins(10, 6, 10, 6)
        total_layout.setSpacing(2)

        total_label = QLabel("مجموع")
        total_label.setStyleSheet(f"""
            font-size: 9px; 
            color: {theme.get('text_secondary')}; 
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        total_label.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(total_label)

        self.lbl_price = QLabel(f"{price:,} تومان")
        self.lbl_price.setStyleSheet(f"""
            QLabel {{
                font-weight: bold;
                color: {theme.get('secondary')};
                font-size: 14px;
                background: transparent;
                border: none;
            }}
        """)
        self.lbl_price.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(self.lbl_price)

        layout.addWidget(total_widget)

        layout.addStretch()

        # دکمه حذف - گرادیانت قرمز
        self.btn_remove = QPushButton("🗑️")
        self.btn_remove.setToolTip("حذف آیتم")
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme.get('error')},
                    stop:1 #F87171);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #DC2626,
                    stop:1 {theme.get('error')});
            }}
            QPushButton:pressed {{
                background-color: #B91C1C;
            }}
        """)
        self.btn_remove.setMaximumWidth(55)
        self.btn_remove.setMinimumHeight(40)
        layout.addWidget(self.btn_remove)

        # Store unit price for calculations
        self._unit_price = unit_price

    def on_quantity_changed(self, new_qty: int):
        """وقتی تعداد تغییر کرد"""
        total_price = self._unit_price * new_qty
        self.lbl_price.setText(f"{total_price:,} تومان")
        
        # Get the actual name without emoji
        name = self.lbl_name.text().replace("🍽️ ", "")
        self.quantity_changed.emit(name, new_qty)
