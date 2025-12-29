# ui/server_settings_dialog.py
"""
Server Settings Dialog for managing the web server configuration
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QFormLayout, QSpinBox, QCheckBox,
    QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from web.server import get_server_runner
from web.config import get_config_manager


class ServerSettingsDialog(QDialog):
    """Dialog for configuring and managing the web server"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.server_runner = get_server_runner()
        self.config_manager = get_config_manager()
        
        self.setWindowTitle("⚙️ تنظیمات سرور وب")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
        self.update_server_status()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Server Status Section
        status_group = QGroupBox("📊 وضعیت سرور")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("وضعیت: متوقف")
        self.status_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        self.url_label = QLabel("آدرس: -")
        self.url_label.setStyleSheet("font-size: 11pt;")
        status_layout.addWidget(self.url_label)
        
        self.network_url_label = QLabel("آدرس شبکه: -")
        self.network_url_label.setStyleSheet("font-size: 11pt;")
        status_layout.addWidget(self.network_url_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ راه‌اندازی سرور")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ توقف سرور")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 10px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        button_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("🔄 راه‌اندازی مجدد")
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #333;
                padding: 10px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: white;
            }
        """)
        button_layout.addWidget(self.restart_btn)
        
        status_layout.addLayout(button_layout)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Configuration Section
        config_group = QGroupBox("🔧 تنظیمات")
        config_layout = QFormLayout()
        
        # Host
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("0.0.0.0 (همه آدرس‌ها)")
        config_layout.addRow("🌐 آدرس میزبان (Host):", self.host_input)
        
        # Port
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(8080)
        config_layout.addRow("🔌 پورت:", self.port_input)
        
        # Auto-start
        self.autostart_checkbox = QCheckBox("راه‌اندازی خودکار با برنامه")
        config_layout.addRow("🚀 راه‌اندازی خودکار:", self.autostart_checkbox)
        
        # Token expiry
        self.token_expire_input = QSpinBox()
        self.token_expire_input.setRange(30, 1440)
        self.token_expire_input.setValue(480)
        self.token_expire_input.setSuffix(" دقیقه")
        config_layout.addRow("⏱️ مدت اعتبار توکن:", self.token_expire_input)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Information Section
        info_group = QGroupBox("ℹ️ راهنما")
        info_layout = QVBoxLayout()
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(150)
        info_text.setHtml("""
            <h4 style="color: #8b4513;">نحوه استفاده:</h4>
            <ul>
                <li><strong>آدرس محلی:</strong> برای دسترسی از همین دستگاه</li>
                <li><strong>آدرس شبکه:</strong> برای دسترسی از دستگاه‌های دیگر در شبکه محلی</li>
                <li><strong>پورت پیش‌فرض:</strong> 8080 (می‌توانید تغییر دهید)</li>
                <li><strong>توجه:</strong> برای دسترسی از شبکه، باید فایروال اجازه دسترسی بدهد</li>
                <li><strong>کاربر پیش‌فرض:</strong> admin / admin123</li>
            </ul>
        """)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 ذخیره تنظیمات")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        bottom_layout.addWidget(self.save_btn)
        
        self.close_btn = QPushButton("❌ بستن")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px 20px;
                font-size: 11pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        bottom_layout.addWidget(self.close_btn)
        
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
        self.server_runner.stop()
    
    def restart_server(self):
        """Restart the web server"""
        if not self.server_runner.is_running:
            self.start_server()
        else:
            self.restart_btn.setEnabled(False)
            self.server_runner.restart()
    
    def update_server_status(self):
        """Update server status display"""
        if self.server_runner.is_running:
            self.status_label.setText("وضعیت: ✅ در حال اجرا")
            self.status_label.setStyleSheet(
                "font-size: 14pt; font-weight: bold; color: #28a745;"
            )
            
            urls = self.server_runner.get_access_urls()
            self.url_label.setText(f"آدرس محلی: {urls['local']}")
            self.network_url_label.setText(f"آدرس شبکه: {urls['network']}")
            
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.restart_btn.setEnabled(True)
        else:
            self.status_label.setText("وضعیت: ⏹️ متوقف")
            self.status_label.setStyleSheet(
                "font-size: 14pt; font-weight: bold; color: #dc3545;"
            )
            
            self.url_label.setText("آدرس: -")
            self.network_url_label.setText("آدرس شبکه: -")
            
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.restart_btn.setEnabled(False)
    
    def on_server_started(self, host, port):
        """Called when server starts"""
        self.update_server_status()
        QMessageBox.information(
            self,
            "✅ موفق",
            f"سرور وب با موفقیت راه‌اندازی شد!\n\n"
            f"آدرس محلی: http://127.0.0.1:{port}\n"
            f"آدرس شبکه: http://{host}:{port}\n\n"
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

