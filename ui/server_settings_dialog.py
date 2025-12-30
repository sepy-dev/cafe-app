# ui/server_settings_dialog.py
"""
Server Settings Dialog for managing the web server configuration
"""
import subprocess
import io
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QFormLayout, QSpinBox, QCheckBox,
    QTextEdit, QMessageBox, QFrame, QWidget, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QImage
from web.server import get_server_runner
from web.config import get_config_manager

# QR Code imports
try:
    import qrcode
    from PIL import Image
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


class ServerSettingsDialog(QDialog):
    """Dialog for configuring and managing the web server"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.server_runner = get_server_runner()
        self.config_manager = get_config_manager()
        
        self.setWindowTitle("⚙️ تنظیمات سرور وب")
        self.setMinimumWidth(700)
        self.setMinimumHeight(700)
        self.setStyleSheet(self.get_dialog_style())
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
        self.update_server_status()
    
    def get_dialog_style(self):
        """Return the main dialog stylesheet"""
        return """
            QDialog {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-size: 13pt;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #ddd;
                border-radius: 10px;
                margin-top: 15px;
                padding: 20px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 20px;
                background-color: white;
                border-radius: 5px;
            }
            QLabel {
                font-size: 11pt;
                color: #333;
            }
            QLineEdit, QSpinBox {
                font-size: 12pt;
                padding: 10px 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: white;
                min-height: 25px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #3498db;
            }
            QCheckBox {
                font-size: 11pt;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
            }
        """
    
    def create_separator(self):
        """Create a horizontal separator line"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #ddd; min-height: 2px; max-height: 2px;")
        return line
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # ==================== Server Status Section ====================
        status_group = QGroupBox("📊 وضعیت سرور")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(15)
        status_layout.setContentsMargins(20, 25, 20, 20)
        
        # Status indicator
        status_container = QWidget()
        status_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        status_inner = QVBoxLayout(status_container)
        status_inner.setSpacing(12)
        status_inner.setContentsMargins(20, 20, 20, 20)
        
        self.status_label = QLabel("وضعیت: ⏹️ متوقف")
        self.status_label.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #dc3545;
            padding: 10px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        status_inner.addWidget(self.status_label)
        
        # URL labels container
        url_container = QWidget()
        url_layout = QVBoxLayout(url_container)
        url_layout.setSpacing(8)
        url_layout.setContentsMargins(0, 10, 0, 0)
        
        self.url_label = QLabel("📍 آدرس محلی: -")
        self.url_label.setStyleSheet("""
            font-size: 12pt;
            color: #555;
            padding: 5px 10px;
            background-color: #e9ecef;
            border-radius: 5px;
        """)
        self.url_label.setAlignment(Qt.AlignCenter)
        url_layout.addWidget(self.url_label)
        
        self.network_url_label = QLabel("🌐 آدرس شبکه: -")
        self.network_url_label.setStyleSheet("""
            font-size: 12pt;
            color: #555;
            padding: 5px 10px;
            background-color: #e9ecef;
            border-radius: 5px;
        """)
        self.network_url_label.setAlignment(Qt.AlignCenter)
        url_layout.addWidget(self.network_url_label)
        
        status_inner.addWidget(url_container)
        
        # QR Code container
        self.qr_container = QWidget()
        qr_layout = QVBoxLayout(self.qr_container)
        qr_layout.setContentsMargins(0, 15, 0, 0)
        qr_layout.setSpacing(10)
        
        qr_title = QLabel("📱 اسکن با گوشی:")
        qr_title.setStyleSheet("font-size: 11pt; font-weight: bold; color: #333;")
        qr_title.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(qr_title)
        
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setStyleSheet("""
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            border: 2px solid #ddd;
        """)
        self.qr_label.setMinimumSize(200, 200)
        self.qr_label.setMaximumSize(200, 200)
        qr_layout.addWidget(self.qr_label, 0, Qt.AlignCenter)
        
        self.qr_container.setVisible(False)  # Hidden by default
        status_inner.addWidget(self.qr_container)
        
        status_layout.addWidget(status_container)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 15, 0, 0)
        
        self.start_btn = QPushButton("▶️ راه‌اندازی سرور")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 15px 25px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ توقف سرور")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 15px 25px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        button_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("🔄 راه‌اندازی مجدد")
        self.restart_btn.setMinimumHeight(50)
        self.restart_btn.setCursor(Qt.PointingHandCursor)
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                padding: 15px 25px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e96b02;
            }
            QPushButton:pressed {
                background-color: #d45e00;
            }
            QPushButton:disabled {
                background-color: #adb5bd;
            }
        """)
        button_layout.addWidget(self.restart_btn)
        
        status_layout.addLayout(button_layout)
        
        # Firewall button
        firewall_layout = QHBoxLayout()
        firewall_layout.setContentsMargins(0, 10, 0, 0)
        
        self.firewall_btn = QPushButton("🛡️ باز کردن فایروال (برای دسترسی از شبکه)")
        self.firewall_btn.setMinimumHeight(45)
        self.firewall_btn.setCursor(Qt.PointingHandCursor)
        self.firewall_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                padding: 12px 20px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
            }
        """)
        self.firewall_btn.clicked.connect(self.open_firewall)
        firewall_layout.addWidget(self.firewall_btn)
        
        status_layout.addLayout(firewall_layout)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # ==================== Configuration Section ====================
        config_group = QGroupBox("🔧 تنظیمات سرور")
        config_layout = QVBoxLayout()
        config_layout.setSpacing(20)
        config_layout.setContentsMargins(20, 25, 20, 20)
        
        # Host setting
        host_container = QHBoxLayout()
        host_container.setSpacing(15)
        
        host_label = QLabel("🌐 آدرس میزبان (Host):")
        host_label.setMinimumWidth(180)
        host_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        host_container.addWidget(host_label)
        
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("0.0.0.0 برای دسترسی از شبکه")
        self.host_input.setMinimumHeight(45)
        host_container.addWidget(self.host_input, 1)
        
        config_layout.addLayout(host_container)
        
        # Port setting
        port_container = QHBoxLayout()
        port_container.setSpacing(15)
        
        port_label = QLabel("🔌 پورت:")
        port_label.setMinimumWidth(180)
        port_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        port_container.addWidget(port_label)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(8080)
        self.port_input.setMinimumHeight(45)
        self.port_input.setMinimumWidth(150)
        port_container.addWidget(self.port_input)
        port_container.addStretch()
        
        config_layout.addLayout(port_container)
        
        # Auto-start setting
        autostart_container = QHBoxLayout()
        autostart_container.setSpacing(15)
        
        autostart_label = QLabel("🚀 راه‌اندازی خودکار:")
        autostart_label.setMinimumWidth(180)
        autostart_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        autostart_container.addWidget(autostart_label)
        
        self.autostart_checkbox = QCheckBox("راه‌اندازی خودکار با اجرای برنامه")
        self.autostart_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 11pt;
                padding: 10px;
            }
        """)
        autostart_container.addWidget(self.autostart_checkbox)
        autostart_container.addStretch()
        
        config_layout.addLayout(autostart_container)
        
        # Token expiry setting
        token_container = QHBoxLayout()
        token_container.setSpacing(15)
        
        token_label = QLabel("⏱️ مدت اعتبار توکن:")
        token_label.setMinimumWidth(180)
        token_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        token_container.addWidget(token_label)
        
        self.token_expire_input = QSpinBox()
        self.token_expire_input.setRange(30, 1440)
        self.token_expire_input.setValue(480)
        self.token_expire_input.setSuffix(" دقیقه")
        self.token_expire_input.setMinimumHeight(45)
        self.token_expire_input.setMinimumWidth(150)
        token_container.addWidget(self.token_expire_input)
        token_container.addStretch()
        
        config_layout.addLayout(token_container)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # ==================== Information Section ====================
        info_group = QGroupBox("ℹ️ راهنمای سریع")
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(20, 25, 20, 20)
        
        info_text = QLabel("""
<div style="line-height: 1.8; font-size: 11pt;">
    <p>• <b>آدرس شبکه:</b> برای دسترسی از دستگاه‌های دیگر در شبکه محلی</p>
    <p>• <b>پورت پیش‌فرض:</b> 8080 (می‌توانید تغییر دهید)</p>
    <p>• <b>توجه:</b> برای دسترسی از شبکه، باید فایروال اجازه دسترسی بدهد</p>
    <p>• <b>کاربر پیش‌فرض:</b> <code style="background: #e9ecef; padding: 2px 8px; border-radius: 4px;">admin</code> / <code style="background: #e9ecef; padding: 2px 8px; border-radius: 4px;">admin123</code></p>
</div>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 8px;
                padding: 15px;
                color: #856404;
            }
        """)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Add stretch to push buttons to bottom
        layout.addStretch()
        
        # ==================== Bottom Buttons ====================
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)
        
        self.save_btn = QPushButton("💾 ذخیره تنظیمات")
        self.save_btn.setMinimumHeight(55)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 15px 30px;
                font-size: 13pt;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)
        bottom_layout.addWidget(self.save_btn, 1)
        
        self.close_btn = QPushButton("❌ بستن")
        self.close_btn.setMinimumHeight(55)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 15px 30px;
                font-size: 13pt;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #494f54;
            }
        """)
        bottom_layout.addWidget(self.close_btn, 1)
        
        layout.addLayout(bottom_layout)
    
    def connect_signals(self):
        """Connect signals to slots"""
        self.start_btn.clicked.connect(self.start_server)
        self.stop_btn.clicked.connect(self.stop_server)
        self.restart_btn.clicked.connect(self.restart_server)
        self.save_btn.clicked.connect(self.save_settings)
        self.close_btn.clicked.connect(self.accept)
        
        # Server signals
        self.server_runner.server_started.connect(self.on_server_started)
        self.server_runner.server_stopped.connect(self.on_server_stopped)
        self.server_runner.server_error.connect(self.on_server_error)
        self.server_runner.status_changed.connect(self.on_status_changed)
    
    def load_settings(self):
        """Load settings from config"""
        config = self.config_manager.config
        self.host_input.setText(config.host)
        self.port_input.setValue(config.port)
        self.autostart_checkbox.setChecked(config.auto_start)
        self.token_expire_input.setValue(config.token_expire_minutes)
    
    def save_settings(self):
        """Save settings to config"""
        try:
            self.config_manager.update(
                host=self.host_input.text(),
                port=self.port_input.value(),
                auto_start=self.autostart_checkbox.isChecked(),
                token_expire_minutes=self.token_expire_input.value()
            )
            
            QMessageBox.information(
                self,
                "✅ موفق",
                "تنظیمات با موفقیت ذخیره شد.\n\n"
                "برای اعمال تغییرات، سرور را راه‌اندازی مجدد کنید."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ خطا",
                f"خطا در ذخیره تنظیمات:\n{str(e)}"
            )
    
    def start_server(self):
        """Start the web server"""
        if self.server_runner.is_running:
            QMessageBox.warning(
                self,
                "⚠️ هشدار",
                "سرور در حال اجرا است"
            )
            return
        
        self.start_btn.setEnabled(False)
        self.start_btn.setText("در حال راه‌اندازی...")
        self.server_runner.start()
    
    def stop_server(self):
        """Stop the web server"""
        if not self.server_runner.is_running:
            QMessageBox.warning(
                self,
                "⚠️ هشدار",
                "سرور در حال اجرا نیست"
            )
            return
        
        self.stop_btn.setEnabled(False)
        self.stop_btn.setText("در حال توقف...")
        self.server_runner.stop()
    
    def restart_server(self):
        """Restart the web server"""
        if not self.server_runner.is_running:
            self.start_server()
        else:
            self.restart_btn.setEnabled(False)
            self.restart_btn.setText("در حال راه‌اندازی مجدد...")
            self.server_runner.restart()
    
    def update_server_status(self):
        """Update server status display"""
        if self.server_runner.is_running:
            self.status_label.setText("✅ سرور در حال اجراست")
            self.status_label.setStyleSheet("""
                font-size: 18pt;
                font-weight: bold;
                color: #28a745;
                padding: 10px;
                background-color: #d4edda;
                border-radius: 8px;
            """)
            
            urls = self.server_runner.get_access_urls()
            self.url_label.setText(f"📍 آدرس محلی: {urls['local']}")
            self.url_label.setStyleSheet("""
                font-size: 12pt;
                color: #155724;
                padding: 8px 15px;
                background-color: #c3e6cb;
                border-radius: 5px;
            """)
            self.network_url_label.setText(f"🌐 آدرس شبکه: {urls['network']}")
            self.network_url_label.setStyleSheet("""
                font-size: 12pt;
                color: #155724;
                padding: 8px 15px;
                background-color: #c3e6cb;
                border-radius: 5px;
            """)
            
            self.start_btn.setEnabled(False)
            self.start_btn.setText("▶️ راه‌اندازی سرور")
            self.stop_btn.setEnabled(True)
            self.stop_btn.setText("⏹️ توقف سرور")
            self.restart_btn.setEnabled(True)
            self.restart_btn.setText("🔄 راه‌اندازی مجدد")
            
            # Show QR code
            self.update_qr_code()
        else:
            self.status_label.setText("⏹️ سرور متوقف است")
            self.status_label.setStyleSheet("""
                font-size: 18pt;
                font-weight: bold;
                color: #dc3545;
                padding: 10px;
                background-color: #f8d7da;
                border-radius: 8px;
            """)
            
            self.url_label.setText("📍 آدرس محلی: -")
            self.url_label.setStyleSheet("""
                font-size: 12pt;
                color: #555;
                padding: 8px 15px;
                background-color: #e9ecef;
                border-radius: 5px;
            """)
            self.network_url_label.setText("🌐 آدرس شبکه: -")
            self.network_url_label.setStyleSheet("""
                font-size: 12pt;
                color: #555;
                padding: 8px 15px;
                background-color: #e9ecef;
                border-radius: 5px;
            """)
            
            self.start_btn.setEnabled(True)
            self.start_btn.setText("▶️ راه‌اندازی سرور")
            self.stop_btn.setEnabled(False)
            self.stop_btn.setText("⏹️ توقف سرور")
            self.restart_btn.setEnabled(False)
            self.restart_btn.setText("🔄 راه‌اندازی مجدد")
            
            # Hide QR code
            self.qr_container.setVisible(False)
    
    def on_server_started(self, host, port):
        """Called when server starts"""
        self.update_server_status()
        QMessageBox.information(
            self,
            "✅ سرور راه‌اندازی شد",
            f"سرور وب با موفقیت راه‌اندازی شد!\n\n"
            f"📍 آدرس محلی: http://127.0.0.1:{port}\n"
            f"🌐 آدرس شبکه: http://{host}:{port}\n\n"
            "اکنون می‌توانید از مرورگر به سیستم دسترسی پیدا کنید."
        )
    
    def on_server_stopped(self):
        """Called when server stops"""
        self.update_server_status()
    
    def on_server_error(self, error):
        """Called when server error occurs"""
        self.update_server_status()
        QMessageBox.critical(
            self,
            "❌ خطای سرور",
            f"خطا در سرور:\n{error}"
        )
    
    def on_status_changed(self, status):
        """Called when server status changes"""
        self.update_server_status()
    
    def generate_qr_code(self, url):
        """Generate QR code for the URL"""
        if not HAS_QRCODE:
            return None
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=2,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert PIL image to QPixmap
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qimage = QImage()
            qimage.loadFromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)
            
            return pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
    
    def update_qr_code(self):
        """Update QR code display"""
        if not self.server_runner.is_running:
            self.qr_container.setVisible(False)
            return
        
        urls = self.server_runner.get_access_urls()
        network_url = urls.get('network', '')
        
        if network_url and HAS_QRCODE:
            pixmap = self.generate_qr_code(network_url)
            if pixmap:
                self.qr_label.setPixmap(pixmap)
                self.qr_container.setVisible(True)
            else:
                self.qr_container.setVisible(False)
        else:
            self.qr_container.setVisible(False)
    
    def open_firewall(self):
        """Open Windows Firewall for the server port"""
        port = self.port_input.value()
        
        reply = QMessageBox.question(
            self,
            "🛡️ باز کردن فایروال",
            f"آیا می‌خواهید پورت {port} را در فایروال ویندوز باز کنید?\n\n"
            "این عملیات نیاز به دسترسی Administrator دارد.\n"
            "پس از تأیید، یک پنجره UAC ظاهر می‌شود.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Create firewall rule using netsh (requires admin)
                rule_name = f"CafeApp_Port_{port}"
                
                # PowerShell command to add firewall rule
                ps_command = f'''
                    $ruleName = "{rule_name}"
                    $existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
                    if ($existingRule) {{
                        Remove-NetFirewallRule -DisplayName $ruleName
                    }}
                    New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow -Profile Any
                '''
                
                # Run as administrator
                result = subprocess.run(
                    ['powershell', '-Command', 
                     f'Start-Process powershell -Verb RunAs -Wait -ArgumentList \'-Command {ps_command}\''],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                QMessageBox.information(
                    self,
                    "✅ موفق",
                    f"قانون فایروال برای پورت {port} ایجاد شد.\n\n"
                    f"نام قانون: {rule_name}\n\n"
                    "اکنون باید بتوانید از دستگاه‌های دیگر به سرور دسترسی پیدا کنید."
                )
                
            except Exception as e:
                # Alternative: Show manual instructions
                QMessageBox.warning(
                    self,
                    "⚠️ خطا",
                    f"خطا در اجرای خودکار:\n{str(e)}\n\n"
                    f"دستور دستی:\n"
                    f"1. Command Prompt را به عنوان Administrator باز کنید\n"
                    f"2. دستور زیر را اجرا کنید:\n\n"
                    f"netsh advfirewall firewall add rule name=\"CafeApp\" dir=in action=allow protocol=TCP localport={port}"
                )
