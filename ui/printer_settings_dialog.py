# ui/printer_settings_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QGroupBox, QMessageBox, QTabWidget, QWidget
)
from infrastructure.printer.receipt_printer import ReceiptPrinter
from ui.styles import ThemeManager, ModernStyles


class PrinterSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.printer = ReceiptPrinter()

        self.setWindowTitle("⚙️ تنظیمات سیستم")
        self.resize(600, 500)

        layout = QVBoxLayout(self)

        # عنوان
        title = QLabel("تنظیمات پیشرفته سیستم")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2; margin-bottom: 10px;")
        layout.addWidget(title)

        # تب‌ها
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # تب پرینتر
        self.setup_printer_tab()

        # تب ظاهر
        self.setup_appearance_tab()

        # تب عمومی
        self.setup_general_tab()

        # دکمه‌های اصلی
        buttons_layout = QHBoxLayout()

        save_btn = QPushButton("💾 ذخیره تنظیمات")
        save_btn.setProperty("class", "success-btn")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)

        cancel_btn = QPushButton("❌ انصراف")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        # بارگذاری تنظیمات فعلی
        self.load_current_settings()

    def setup_printer_tab(self):
        """Setup printer settings tab"""
        printer_tab = QWidget()
        layout = QVBoxLayout(printer_tab)

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

        layout.addStretch()
        self.tabs.addTab(printer_tab, "🖨️ پرینتر")

    def setup_appearance_tab(self):
        """Setup appearance settings tab"""
        appearance_tab = QWidget()
        layout = QVBoxLayout(appearance_tab)

        # انتخاب تم
        theme_group = QGroupBox("تم برنامه")
        theme_layout = QVBoxLayout(theme_group)

        theme_layout.addWidget(QLabel("انتخاب تم:"))

        self.theme_combo = QComboBox()
        themes = ThemeManager.get_available_themes()
        for theme_name in themes.keys():
            display_name = {
                "modern_blue": "🔵 مدرن آبی",
                "dark_mode": "🌙 حالت تاریک",
                "warm_orange": "🟠 گرم نارنجی"
            }.get(theme_name, theme_name)
            self.theme_combo.addItem(display_name, theme_name)

        self.theme_combo.currentTextChanged.connect(self.preview_theme)
        theme_layout.addWidget(self.theme_combo)

        preview_btn = QPushButton("👁️ پیش‌نمایش")
        preview_btn.clicked.connect(self.preview_theme)
        theme_layout.addWidget(preview_btn)

        layout.addWidget(theme_group)

        # تنظیمات فونت
        font_group = QGroupBox("تنظیمات فونت")
        font_layout = QVBoxLayout(font_group)

        font_layout.addWidget(QLabel("تنظیمات فونت در نسخه‌های بعدی اضافه خواهد شد."))

        layout.addWidget(font_group)

        layout.addStretch()
        self.tabs.addTab(appearance_tab, "🎨 ظاهر")

    def setup_general_tab(self):
        """Setup general settings tab"""
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)

        # اطلاعات سیستم
        info_group = QGroupBox("اطلاعات سیستم")
        info_layout = QVBoxLayout(info_group)

        info_text = """
        🍽️ سیستم مدیریت کافه
        نسخه: 2.0 - مدرن
        توسعه‌دهنده: AI Assistant

        ویژگی‌های اصلی:
        • مدیریت جداگانه سفارشات میزها
        • رابط کاربری مدرن و زیبا
        • پشتیبان‌گیری و بازیابی
        • چاپ فاکتور پیشرفته
        • گزارش‌گیری با نمودار
        """
        info_label = QLabel(info_text.strip())
        info_label.setStyleSheet("line-height: 1.6;")
        info_layout.addWidget(info_label)

        layout.addWidget(info_group)

        layout.addStretch()
        self.tabs.addTab(general_tab, "ℹ️ عمومی")

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

    def preview_theme(self):
        """پیش‌نمایش تم انتخاب شده"""
        theme_name = self.theme_combo.currentData()
        if theme_name:
            ThemeManager.apply_theme(theme_name)
            # اعمال استایل جدید
            if self.parent():
                self.parent().setStyleSheet(ModernStyles.get_main_style())
            QMessageBox.information(self, "تم تغییر کرد", f"تم '{self.theme_combo.currentText()}' اعمال شد!")

    def save_settings(self):
        """ذخیره تنظیمات"""
        # ذخیره تنظیمات پرینتر
        selected_printer = self.printer_combo.currentText()
        self.printer.set_printer(selected_printer)

        # ذخیره تم انتخاب شده
        selected_theme = self.theme_combo.currentData()
        if selected_theme:
            ThemeManager.apply_theme(selected_theme)
            if self.parent():
                self.parent().setStyleSheet(ModernStyles.get_main_style())

        QMessageBox.information(
            self, "موفق",
            f"تنظیمات ذخیره شد:\nپرینتر: {selected_printer}\nتم: {self.theme_combo.currentText()}"
        )
        self.accept()
