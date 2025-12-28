# ui/printer_settings_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QMessageBox
)
from infrastructure.printer.receipt_printer import ReceiptPrinter


class PrinterSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.printer = ReceiptPrinter()

        self.setWindowTitle("تنظیمات پرینتر")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # عنوان
        title = QLabel("تنظیمات پرینتر فاکتور")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # انتخاب پرینتر
        printer_group = QGroupBox("انتخاب پرینتر")
        printer_layout = QVBoxLayout(printer_group)

        self.printer_combo = QComboBox()
        self.load_printers()
        printer_layout.addWidget(QLabel("پرینتر:"))
        printer_layout.addWidget(self.printer_combo)

        refresh_btn = QPushButton("🔄 بروزرسانی لیست")
        refresh_btn.clicked.connect(self.load_printers)
        printer_layout.addWidget(refresh_btn)

        layout.addWidget(printer_group)

        # تست پرینتر
        test_group = QGroupBox("تست پرینتر")
        test_layout = QVBoxLayout(test_group)

        self.test_print_btn = QPushButton("🖨️ چاپ فاکتور تست")
        self.test_print_btn.clicked.connect(self.test_printer)
        test_layout.addWidget(self.test_print_btn)

        layout.addWidget(test_group)

        # دکمه‌های اصلی
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton("💾 ذخیره تنظیمات")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)

        cancel_btn = QPushButton("❌ انصراف")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        # بارگذاری تنظیمات فعلی
        self.load_current_settings()

    def load_printers(self):
        """بارگذاری لیست پرینترهای موجود"""
        self.printer_combo.clear()
        printers = self.printer.get_available_printers()
        self.printer_combo.addItems(printers)

    def load_current_settings(self):
        """بارگذاری تنظیمات فعلی"""
        if self.printer.printer_name:
            index = self.printer_combo.findText(self.printer.printer_name)
            if index >= 0:
                self.printer_combo.setCurrentIndex(index)

    def save_settings(self):
        """ذخیره تنظیمات"""
        selected_printer = self.printer_combo.currentText()
        self.printer.set_printer(selected_printer)

        QMessageBox.information(
            self, "موفق",
            f"تنظیمات پرینتر ذخیره شد:\n{selected_printer}"
        )
        self.accept()

    def test_printer(self):
        """چاپ فاکتور تست"""
        try:
            self.printer.print_test_receipt()
            QMessageBox.information(self, "موفق", "فاکتور تست با موفقیت ارسال شد به پرینتر")
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در تست پرینتر:\n{str(e)}")
