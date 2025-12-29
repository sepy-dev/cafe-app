import sys
import os

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

# راه‌اندازی دیتابیس
from infrastructure.database.session import init_db
init_db()

# وارد کردن مدل کاربر برای ایجاد جدول
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.base import Base
from infrastructure.database.session import engine
Base.metadata.create_all(bind=engine)

app = QApplication(sys.argv)

# تنظیمات برنامه
app.setApplicationName("سیستم مدیریت کافه")
app.setOrganizationName("CafeApp")

# نمایش صفحه لاگین
from ui.login_dialog import LoginDialog
login_dialog = LoginDialog()

if login_dialog.exec():
    # لاگین موفق - نمایش پنجره اصلی
    from ui.main_window import POSMainWindow
    window = POSMainWindow()
    
    # نمایش نام کاربر
    user = login_dialog.logged_in_user
    if user:
        window.setWindowTitle(f"🍽️ سیستم ثبت سفارش کافه - {user.full_name}")
    
    window.show()
    sys.exit(app.exec())
else:
    # لاگین لغو شد
    sys.exit(0)
