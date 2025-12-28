# ui/add_customer_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox
)


class AddCustomerDialog(QDialog):
    """Dialog for adding new customers"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("افزودن مشتری جدید")
        self.resize(400, 250)

        layout = QVBoxLayout(self)

        # Title
        title = QLabel("افزودن مشتری جدید به باشگاه مشتریان")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Customer name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("نام و نام خانوادگی:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("مثال: احمد رضایی")
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        # Phone number
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(QLabel("شماره تماس:"))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("مثال: 09123456789")
        phone_layout.addWidget(self.phone_input)
        form_layout.addLayout(phone_layout)

        # Email (optional)
        email_layout = QHBoxLayout()
        email_layout.addWidget(QLabel("ایمیل (اختیاری):"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("customer@example.com")
        email_layout.addWidget(self.email_input)
        form_layout.addLayout(email_layout)

        layout.addLayout(form_layout)

        # Info text
        info_label = QLabel(
            "💡 مشتریان جدید با 50 امتیاز هدیه شروع می‌کنند!\n"
            "هر 10 تومان خرید = 1 امتیاز"
        )
        info_label.setStyleSheet("color: #64748B; font-size: 11px; margin: 10px 0;")
        layout.addWidget(info_label)

        # Buttons
        buttons_layout = QHBoxLayout()

        cancel_btn = QPushButton("❌ انصراف")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        add_btn = QPushButton("✅ افزودن مشتری")
        add_btn.clicked.connect(self.add_customer)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        buttons_layout.addWidget(add_btn)

        layout.addLayout(buttons_layout)

    def add_customer(self):
        """Add the customer"""
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not name:
            QMessageBox.warning(self, "خطا", "لطفاً نام مشتری را وارد کنید")
            return

        if not phone:
            QMessageBox.warning(self, "خطا", "لطفاً شماره تماس را وارد کنید")
            return

        # Basic phone validation
        if not phone.startswith('09') or len(phone) != 11:
            QMessageBox.warning(self, "خطا", "شماره تماس باید با 09 شروع شود و 11 رقم باشد")
            return

        # Here you would save to database
        # For now, just show success
        QMessageBox.information(
            self, "موفق",
            f"مشتری '{name}' با موفقیت اضافه شد!\n\n"
            f"امتیاز هدیه: 50 امتیاز\n"
            f"سطح: برنزی"
        )
        self.accept()
