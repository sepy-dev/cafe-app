# ui/backup_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox,
    QProgressBar, QTextEdit, QFileDialog
)
from PySide6.QtCore import QThread, Signal, Qt
from datetime import datetime
from infrastructure.backup_service import BackupService


class BackupWorker(QThread):
    """Thread برای انجام عملیات پشتیبان‌گیری و بازیابی"""
    finished = Signal(str)  # نتیجه عملیات
    error = Signal(str)     # خطا
    progress = Signal(str)  # پیشرفت عملیات

    def __init__(self, operation, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
        self.backup_service = BackupService()

    def run(self):
        try:
            if self.operation == "backup":
                self.progress.emit("در حال ایجاد پشتیبان...")
                result = self.backup_service.create_backup(**self.kwargs)
                self.finished.emit(f"پشتیبان با موفقیت ایجاد شد:\n{result}")

            elif self.operation == "restore":
                self.progress.emit("در حال بازیابی پشتیبان...")
                self.backup_service.restore_backup(**self.kwargs)
                self.finished.emit("پشتیبان با موفقیت بازیابی شد")

        except Exception as e:
            self.error.emit(str(e))


class BackupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backup_service = BackupService()

        self.setWindowTitle("مدیریت پشتیبان")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        # عنوان
        title = QLabel("مدیریت پشتیبان‌های سیستم")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # بخش ایجاد پشتیبان
        backup_group_layout = QHBoxLayout()

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("توضیح پشتیبان (اختیاری)")
        backup_group_layout.addWidget(QLabel("توضیح:"))
        backup_group_layout.addWidget(self.description_input)

        self.create_backup_btn = QPushButton("💾 ایجاد پشتیبان")
        self.create_backup_btn.clicked.connect(self.create_backup)
        backup_group_layout.addWidget(self.create_backup_btn)

        layout.addLayout(backup_group_layout)

        # جدول لیست پشتیبان‌ها
        self.backups_table = QTableWidget()
        self.backups_table.setColumnCount(4)
        self.backups_table.setHorizontalHeaderLabels(["نام فایل", "تاریخ ایجاد", "حجم (MB)", "عملیات"])
        self.backups_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.backups_table)

        # دکمه‌های مدیریت پشتیبان
        buttons_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("🔄 بروزرسانی لیست")
        self.refresh_btn.clicked.connect(self.load_backups)
        buttons_layout.addWidget(self.refresh_btn)

        self.restore_btn = QPushButton("📁 بازیابی پشتیبان")
        self.restore_btn.clicked.connect(self.restore_backup)
        buttons_layout.addWidget(self.restore_btn)

        self.delete_btn = QPushButton("🗑️ حذف پشتیبان")
        self.delete_btn.clicked.connect(self.delete_backup)
        buttons_layout.addWidget(self.delete_btn)

        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

        # نوار پیشرفت
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # ناحیه پیام‌ها
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(100)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.load_backups()

    def load_backups(self):
        """بارگذاری لیست پشتیبان‌ها"""
        backups = self.backup_service.list_backups()

        self.backups_table.setRowCount(len(backups))
        for row, backup in enumerate(backups):
            self.backups_table.setItem(row, 0, QTableWidgetItem(backup["filename"]))
            self.backups_table.setItem(row, 1, QTableWidgetItem(
                backup["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.backups_table.setItem(row, 2, QTableWidgetItem(str(backup["size_mb"])))

            # دکمه عملیات
            actions_layout = QHBoxLayout()
            restore_btn = QPushButton("بازیابی")
            restore_btn.clicked.connect(lambda _, path=backup["path"]: self.restore_specific_backup(path))
            actions_layout.addWidget(restore_btn)

            delete_btn = QPushButton("حذف")
            delete_btn.clicked.connect(lambda _, filename=backup["filename"]: self.delete_specific_backup(filename))
            actions_layout.addWidget(delete_btn)

            # ایجاد ویجت container برای دکمه‌ها
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.backups_table.setCellWidget(row, 3, actions_widget)

        self.backups_table.resizeColumnsToContents()

    def create_backup(self):
        """ایجاد پشتیبان جدید"""
        description = self.description_input.text().strip()

        # غیرفعال کردن دکمه‌ها
        self.create_backup_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # حالت نامحدود

        # اجرای عملیات در thread جداگانه
        self.worker = BackupWorker("backup", description=description)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_backup_finished)
        self.worker.error.connect(self.on_backup_error)
        self.worker.start()

    def restore_backup(self):
        """انتخاب فایل پشتیبان برای بازیابی"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "انتخاب فایل پشتیبان", "", "فایل‌های پشتیبان (*.zip)"
        )

        if file_path:
            self.restore_specific_backup(file_path)

    def restore_specific_backup(self, backup_path: str):
        """بازیابی پشتیبان خاص"""
        reply = QMessageBox.question(
            self, "تأیید بازیابی",
            "⚠️ هشدار: این عملیات تمام داده‌های فعلی را جایگزین خواهد کرد.\n\n"
            "آیا مطمئن هستید که می‌خواهید ادامه دهید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # غیرفعال کردن دکمه‌ها
            self.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)

            # اجرای عملیات در thread جداگانه
            self.worker = BackupWorker("restore", backup_file=backup_path)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.on_restore_finished)
            self.worker.error.connect(self.on_restore_error)
            self.worker.start()

    def delete_backup(self):
        """انتخاب پشتیبان برای حذف"""
        selected_rows = set()
        for item in self.backups_table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            QMessageBox.warning(self, "خطا", "لطفاً یک پشتیبان را انتخاب کنید")
            return

        row = list(selected_rows)[0]
        filename = self.backups_table.item(row, 0).text()
        self.delete_specific_backup(filename)

    def delete_specific_backup(self, filename: str):
        """حذف پشتیبان خاص"""
        reply = QMessageBox.question(
            self, "تأیید حذف",
            f"آیا مطمئن هستید که می‌خواهید پشتیبان '{filename}' را حذف کنید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.backup_service.delete_backup(filename)
                self.log_message(f"پشتیبان '{filename}' با موفقیت حذف شد")
                self.load_backups()
            except Exception as e:
                QMessageBox.warning(self, "خطا", f"خطا در حذف پشتیبان: {str(e)}")

    def update_progress(self, message: str):
        """به‌روزرسانی نوار پیشرفت"""
        self.log_message(message)

    def on_backup_finished(self, message: str):
        """پایان عملیات پشتیبان‌گیری"""
        self.progress_bar.setVisible(False)
        self.create_backup_btn.setEnabled(True)
        self.log_message(message)
        QMessageBox.information(self, "موفق", message)
        self.load_backups()

    def on_backup_error(self, error_msg: str):
        """خطا در پشتیبان‌گیری"""
        self.progress_bar.setVisible(False)
        self.create_backup_btn.setEnabled(True)
        self.log_message(f"خطا: {error_msg}")
        QMessageBox.warning(self, "خطا", f"خطا در ایجاد پشتیبان:\n{error_msg}")

    def on_restore_finished(self, message: str):
        """پایان عملیات بازیابی"""
        self.progress_bar.setVisible(False)
        self.setEnabled(True)
        self.log_message(message)
        QMessageBox.information(self, "موفق", message)

        # بروزرسانی رابط کاربری
        self.parent().menu_view.load_menu()
        self.parent().order_view.refresh_ui()

    def on_restore_error(self, error_msg: str):
        """خطا در بازیابی"""
        self.progress_bar.setVisible(False)
        self.setEnabled(True)
        self.log_message(f"خطا: {error_msg}")
        QMessageBox.warning(self, "خطا", f"خطا در بازیابی پشتیبان:\n{error_msg}")

    def log_message(self, message: str):
        """افزودن پیام به لاگ"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
