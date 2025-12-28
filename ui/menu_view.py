#menu_view
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QHBoxLayout, QPushButton, QComboBox, QGroupBox, QScrollArea,
    QFrame, QGridLayout
)
from PySide6.QtCore import Signal, Qt

from application.menu_service import MenuService

class MenuView(QWidget):
    product_selected = Signal(int)  # product_id

    def __init__(self):
        super().__init__()

        self.menu_service = MenuService()
        self.current_category = "همه"

        layout = QVBoxLayout(self)

        # عنوان
        title = QLabel("🍽️ منوی کافه")
        title.setStyleSheet("font-size:18px; font-weight:bold; color: #2E7D32;")
        layout.addWidget(title)

        # انتخاب دسته‌بندی
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("دسته‌بندی:"))

        self.category_combo = QComboBox()
        self.category_combo.addItem("همه")
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        category_layout.addWidget(self.category_combo)

        self.refresh_btn = QPushButton("🔄 بروزرسانی")
        self.refresh_btn.clicked.connect(self.load_menu)
        category_layout.addWidget(self.refresh_btn)

        category_layout.addStretch()
        layout.addLayout(category_layout)

        # اسکرول area برای محصولات
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.products_widget = QWidget()
        self.products_layout = QVBoxLayout(self.products_widget)
        self.products_layout.setSpacing(10)

        scroll_area.setWidget(self.products_widget)
        layout.addWidget(scroll_area)

        self.load_menu()
        self.update_categories()

    def update_categories(self):
        """به‌روزرسانی لیست دسته‌بندی‌ها"""
        self.category_combo.clear()
        self.category_combo.addItem("همه")

        categories = self.menu_service.get_categories()
        for category in sorted(categories):
            self.category_combo.addItem(category)

    def on_category_changed(self, category: str):
        """وقتی دسته‌بندی تغییر کرد"""
        self.current_category = category
        self.load_menu()

    def load_menu(self):
        """بارگذاری محصولات"""
        # پاک کردن محصولات قبلی
        while self.products_layout.count():
            child = self.products_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # دریافت محصولات
        if self.current_category == "همه":
            products = self.menu_service.get_active_products()
        else:
            products = self.menu_service.get_products_by_category(self.current_category)

        # گروه‌بندی محصولات در ردیف‌های ۲ تایی
        row_layout = None
        for i, product in enumerate(products):
            if i % 2 == 0:
                # ردیف جدید شروع کن
                row_layout = QHBoxLayout()
                row_layout.setSpacing(10)
                self.products_layout.addLayout(row_layout)

            # ایجاد کارت محصول
            product_card = self.create_product_card(product)
            row_layout.addWidget(product_card)

        # اگر تعداد محصولات فرد باشد، فضای خالی اضافه کن
        if len(products) % 2 == 1:
            row_layout.addStretch()

        self.products_layout.addStretch()

    def create_product_card(self, product) -> QWidget:
        """ایجاد کارت محصول مدرن"""
        card = QWidget()
        card.setObjectName("product-card")
        card.setProperty("class", "product-card")
        card.setMinimumSize(150, 140)
        card.setMaximumSize(180, 170)
        from PySide6.QtWidgets import QSizePolicy
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        card.setStyleSheet("""
            QWidget[class="product-card"] {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                margin: 5px;
            }
            QWidget[class="product-card"]:hover {
                border-color: #2196F3;
                background-color: #F8F9FA;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # نام محصول
        name_label = QLabel(product.name)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1976D2;
                text-align: center;
                margin-bottom: 5px;
            }
        """)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # دسته‌بندی
        category_label = QLabel(f"📂 {product.category}")
        category_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #666666;
                background-color: #F5F5F5;
                padding: 4px 8px;
                border-radius: 10px;
                text-align: center;
            }
        """)
        category_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(category_label)

        # قیمت
        price_label = QLabel(f"💰 {product.price:,} تومان")
        price_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #FF6F00;
                text-align: center;
                margin: 5px 0;
            }
        """)
        price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(price_label)

        layout.addStretch()

        # دکمه افزودن
        add_btn = QPushButton("🛒 افزودن به سفارش")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-weight: bold;
                font-size: 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #3D8B40;
            }
        """)
        add_btn.clicked.connect(lambda: self.product_selected.emit(product.id))
        layout.addWidget(add_btn)

        return card
