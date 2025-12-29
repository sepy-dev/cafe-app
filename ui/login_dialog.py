# ui/login_dialog.py - Beautiful Modern Login Dialog
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QStackedWidget, QWidget,
    QGraphicsDropShadowEffect, QApplication
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor

from application.auth_service import AuthService
from ui.styles import ThemeManager


class LoginDialog(QDialog):
    """Modern beautiful login/register dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_service = AuthService()
        self.theme = ThemeManager().current_theme
        self.logged_in_user = None
        
        self.setWindowTitle("🔐 ورود به سیستم")
        self.setFixedSize(520, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # Set proper font for Persian text
        app_font = QFont("Segoe UI", 12)
        app_font.setStyleHint(QFont.StyleHint.SansSerif)
        self.setFont(app_font)
        
        self.setup_ui()
        self.apply_styles()
        
        # Check if first time (no users)
        if not self.auth_service.has_users():
            self.show_register_page()
    
    def setup_ui(self):
        """Setup the UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Main container with shadow
        container = QFrame()
        container.setObjectName("mainContainer")
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(45, 45, 45, 35)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeBtn")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.reject)
        close_layout.addWidget(close_btn)
        container_layout.addLayout(close_layout)
        
        # Header with animated logo
        header_layout = QVBoxLayout()
        header_layout.setSpacing(12)
        
        # Logo container with gradient background
        logo_container = QWidget()
        logo_container.setObjectName("logoContainer")
        logo_container.setFixedSize(100, 100)
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        
        logo_label = QLabel("☕")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("font-size: 50px; background: transparent;")
        logo_layout.addWidget(logo_label)
        
        logo_wrapper = QHBoxLayout()
        logo_wrapper.addStretch()
        logo_wrapper.addWidget(logo_container)
        logo_wrapper.addStretch()
        header_layout.addLayout(logo_wrapper)
        
        title_label = QLabel("کافه‌شاپ من")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {self.theme.get('text_primary')}; background: transparent;")
        header_layout.addWidget(title_label)
        
        self.subtitle_label = QLabel("خوش آمدید! لطفاً وارد شوید")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setObjectName("subtitle")
        self.subtitle_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-size: 14px; background: transparent;")
        header_layout.addWidget(self.subtitle_label)
        
        container_layout.addLayout(header_layout)
        container_layout.addSpacing(10)
        
        # Stacked widget for login/register
        self.stacked = QStackedWidget()
        
        # Login page
        self.login_page = self.create_login_page()
        self.stacked.addWidget(self.login_page)
        
        # Register page
        self.register_page = self.create_register_page()
        self.stacked.addWidget(self.register_page)
        
        container_layout.addWidget(self.stacked)
        
        # Footer
        container_layout.addSpacing(15)
        footer_label = QLabel("نسخه 2.0 - سیستم مدیریت کافه")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet(f"color: {self.theme.get('text_tertiary')}; font-size: 11px; background: transparent;")
        container_layout.addWidget(footer_label)
        
        main_layout.addWidget(container)
    
    def create_login_page(self) -> QWidget:
        """Create login page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(18)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Username field
        username_layout = QVBoxLayout()
        username_layout.setSpacing(6)
        username_label = QLabel("نام کاربری 👤")
        username_label.setAlignment(Qt.AlignRight)
        username_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-weight: bold; font-size: 13px; background: transparent;")
        username_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("نام کاربری خود را وارد کنید")
        self.username_input.setMinimumHeight(50)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_layout.setSpacing(6)
        password_label = QLabel("رمز عبور 🔒")
        password_label.setAlignment(Qt.AlignRight)
        password_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-weight: bold; font-size: 13px; background: transparent;")
        password_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور خود را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.returnPressed.connect(self.do_login)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        layout.addSpacing(5)
        
        # Login button
        self.login_btn = QPushButton("🚀 ورود به سیستم")
        self.login_btn.setMinimumHeight(55)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.do_login)
        self.login_btn.setObjectName("primaryBtn")
        layout.addWidget(self.login_btn)
        
        # Divider
        divider_layout = QHBoxLayout()
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet(f"background-color: {self.theme.get('border_light')};")
        divider_layout.addWidget(line1)
        
        or_label = QLabel("یا")
        or_label.setStyleSheet(f"color: {self.theme.get('text_tertiary')}; padding: 0 15px; background: transparent;")
        divider_layout.addWidget(or_label)
        
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet(f"background-color: {self.theme.get('border_light')};")
        divider_layout.addWidget(line2)
        
        layout.addLayout(divider_layout)
        
        # Register link
        register_btn = QPushButton("📝 ایجاد حساب کاربری جدید")
        register_btn.setObjectName("secondaryBtn")
        register_btn.setMinimumHeight(48)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.clicked.connect(self.show_register_page)
        layout.addWidget(register_btn)
        
        return page
    
    def create_register_page(self) -> QWidget:
        """Create register page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(25)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Full name field
        name_layout = QVBoxLayout()
        name_layout.setSpacing(10)
        name_label = QLabel("📝 نام کامل")
        name_label.setAlignment(Qt.AlignRight)
        name_label.setFixedHeight(24)
        name_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-weight: bold; font-size: 14px; background: transparent; padding: 2px 0;")
        name_layout.addWidget(name_label)
        
        self.reg_name_input = QLineEdit()
        self.reg_name_input.setPlaceholderText("نام و نام خانوادگی")
        self.reg_name_input.setFixedHeight(48)
        name_layout.addWidget(self.reg_name_input)
        layout.addLayout(name_layout)
        
        # Username field
        username_layout = QVBoxLayout()
        username_layout.setSpacing(10)
        username_label = QLabel("👤 نام کاربری")
        username_label.setAlignment(Qt.AlignRight)
        username_label.setFixedHeight(24)
        username_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-weight: bold; font-size: 14px; background: transparent; padding: 2px 0;")
        username_layout.addWidget(username_label)
        
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("یک نام کاربری انتخاب کنید")
        self.reg_username_input.setFixedHeight(48)
        username_layout.addWidget(self.reg_username_input)
        layout.addLayout(username_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_layout.setSpacing(10)
        password_label = QLabel("🔒 رمز عبور")
        password_label.setAlignment(Qt.AlignRight)
        password_label.setFixedHeight(24)
        password_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-weight: bold; font-size: 14px; background: transparent; padding: 2px 0;")
        password_layout.addWidget(password_label)
        
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("حداقل ۴ کاراکتر")
        self.reg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password_input.setFixedHeight(48)
        password_layout.addWidget(self.reg_password_input)
        layout.addLayout(password_layout)
        
        # Confirm password field
        confirm_layout = QVBoxLayout()
        confirm_layout.setSpacing(10)
        confirm_label = QLabel("🔒 تکرار رمز عبور")
        confirm_label.setAlignment(Qt.AlignRight)
        confirm_label.setFixedHeight(24)
        confirm_label.setStyleSheet(f"color: {self.theme.get('text_secondary')}; font-weight: bold; font-size: 14px; background: transparent; padding: 2px 0;")
        confirm_layout.addWidget(confirm_label)
        
        self.reg_confirm_input = QLineEdit()
        self.reg_confirm_input.setPlaceholderText("رمز عبور را دوباره وارد کنید")
        self.reg_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_confirm_input.setFixedHeight(48)
        self.reg_confirm_input.returnPressed.connect(self.do_register)
        confirm_layout.addWidget(self.reg_confirm_input)
        layout.addLayout(confirm_layout)
        
        layout.addSpacing(20)
        
        # Register button
        self.register_btn = QPushButton("✅ ایجاد حساب کاربری")
        self.register_btn.setMinimumHeight(52)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.clicked.connect(self.do_register)
        self.register_btn.setObjectName("primaryBtn")
        layout.addWidget(self.register_btn)
        
        # Back to login
        back_btn = QPushButton("← بازگشت به صفحه ورود")
        back_btn.setObjectName("linkBtn")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.show_login_page)
        layout.addWidget(back_btn)
        
        return page
    
    def apply_styles(self):
        """Apply modern styles"""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: transparent;
            }}
            
            #mainContainer {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.get('bg_main')},
                    stop:0.5 {self.theme.get('bg_card')},
                    stop:1 {self.theme.get('bg_secondary')});
                border: 1px solid {self.theme.get('border_light')};
                border-radius: 24px;
            }}
            
            #logoContainer {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.theme.get('primary')},
                    stop:1 {self.theme.get('primary_light')});
                border-radius: 50px;
            }}
            
            #closeBtn {{
                background-color: {self.theme.get('bg_tertiary')};
                color: {self.theme.get('text_secondary')};
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }}
            
            #closeBtn:hover {{
                background-color: {self.theme.get('error')};
                color: white;
            }}
            
            QLineEdit {{
                border: 2px solid {self.theme.get('border_light')};
                border-radius: 14px;
                padding: 12px 16px;
                font-size: 13px;
                font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
                background-color: {self.theme.get('bg_input')};
                color: {self.theme.get('text_primary')};
                selection-background-color: {self.theme.get('primary')};
                selection-color: white;
            }}
            
            QLineEdit:focus {{
                border-color: {self.theme.get('primary')};
                background-color: {self.theme.get('bg_main')};
            }}
            
            QLineEdit::placeholder {{
                color: {self.theme.get('text_tertiary')};
                font-style: italic;
            }}
            
            #primaryBtn {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.theme.get('primary')},
                    stop:1 {self.theme.get('primary_light')});
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }}
            
            #primaryBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.theme.get('primary_light')},
                    stop:1 {self.theme.get('primary')});
            }}
            
            #primaryBtn:pressed {{
                background-color: {self.theme.get('primary_dark')};
            }}
            
            #secondaryBtn {{
                background-color: {self.theme.get('bg_tertiary')};
                color: {self.theme.get('text_primary')};
                border: 2px solid {self.theme.get('border_light')};
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
            }}
            
            #secondaryBtn:hover {{
                background-color: {self.theme.get('bg_hover')};
                border-color: {self.theme.get('primary')};
                color: {self.theme.get('primary')};
            }}
            
            #linkBtn {{
                background: transparent;
                color: {self.theme.get('primary')};
                border: none;
                font-weight: bold;
                font-size: 13px;
                padding: 10px;
            }}
            
            #linkBtn:hover {{
                color: {self.theme.get('primary_light')};
                text-decoration: underline;
            }}
        """)
    
    def show_login_page(self):
        """Show login page"""
        self.stacked.setCurrentIndex(0)
        self.subtitle_label.setText("خوش آمدید! لطفاً وارد شوید")
    
    def show_register_page(self):
        """Show register page"""
        self.stacked.setCurrentIndex(1)
        self.subtitle_label.setText("ایجاد حساب کاربری جدید")
    
    def do_login(self):
        """Perform login"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "خطا", "⚠️ لطفاً نام کاربری و رمز عبور را وارد کنید")
            return
        
        success, message = self.auth_service.login(username, password)
        
        if success:
            self.logged_in_user = AuthService.get_current_user()
            self.accept()
        else:
            QMessageBox.warning(self, "خطا در ورود", f"❌ {message}")
    
    def do_register(self):
        """Perform registration"""
        full_name = self.reg_name_input.text().strip()
        username = self.reg_username_input.text().strip()
        password = self.reg_password_input.text()
        confirm = self.reg_confirm_input.text()
        
        if not all([full_name, username, password, confirm]):
            QMessageBox.warning(self, "خطا", "⚠️ لطفاً تمام فیلدها را پر کنید")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "خطا", "⚠️ رمز عبور و تکرار آن مطابقت ندارند")
            return
        
        # First user is admin
        role = "admin" if not self.auth_service.has_users() else "cashier"
        
        success, message = self.auth_service.register(username, password, full_name, role)
        
        if success:
            QMessageBox.information(self, "موفق", f"✅ {message}\n\nاکنون می‌توانید وارد شوید.")
            self.show_login_page()
            self.username_input.setText(username)
            self.password_input.setFocus()
        else:
            QMessageBox.warning(self, "خطا در ثبت‌نام", f"❌ {message}")
    
    def mousePressEvent(self, event):
        """Enable window dragging"""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if event.buttons() == Qt.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
