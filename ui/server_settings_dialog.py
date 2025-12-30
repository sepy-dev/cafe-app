# ui/server_settings_dialog.py
"""
Server Settings Dialog for managing the web server configuration
"""
import subprocess
import io
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QSpinBox, QCheckBox,
    QMessageBox, QFrame, QScrollArea, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from web.server import get_server_runner
from web.config import get_config_manager


# QR Code imports
try:
    import qrcode
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
        self.setMinimumSize(500, 600)
        self.resize(550, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
        """)
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
        self.update_server_status()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # Content Widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # ==================== Server Status Section ====================
        status_group = self.create_group("📊 وضعیت سرور")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(12)
        
        # Status Label
        self.status_label = QLabel("⏹️ سرور متوقف است")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMinimumHeight(50)
        self.update_status_style(False)
        status_layout.addWidget(self.status_label)
        
        # URL Labels
        self.url_label = QLabel("📍 آدرس محلی: -")
        self.url_label.setStyleSheet(self.get_url_label_style())
        self.url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.url_label.setWordWrap(True)
        status_layout.addWidget(self.url_label)
        
        self.network_url_label = QLabel("🌐 آدرس شبکه: -")
        self.network_url_label.setStyleSheet(self.get_url_label_style())
        self.network_url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.network_url_label.setWordWrap(True)
        status_layout.addWidget(self.network_url_label)
        
        # QR Code Frame
        self.qr_frame = QFrame()
        self.qr_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #28a745;
                border-radius: 12px;
            }
        """)
        self.qr_frame.setVisible(False)
        qr_layout = QVBoxLayout(self.qr_frame)
        qr_layout.setContentsMargins(20, 16, 20, 20)
        qr_layout.setSpacing(12)
        
        qr_title = QLabel("📱 QR Code - اسکن با موبایل")
        qr_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #28a745; background: transparent; border: none;")
        qr_title.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(qr_title)
        
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setFixedSize(220, 220)
        self.qr_label.setStyleSheet("background-color: white; border: none;")
        qr_layout.addWidget(self.qr_label, 0, Qt.AlignCenter)
        
        status_layout.addWidget(self.qr_frame)
        
        # Control Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        self.start_btn = self.create_button("▶️ راه‌اندازی", "#28a745", "#1e7e34")
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = self.create_button("⏹️ توقف", "#dc3545", "#c82333")
        btn_layout.addWidget(self.stop_btn)
        
        self.restart_btn = self.create_button("🔄 ریستارت", "#fd7e14", "#e96b02")
        btn_layout.addWidget(self.restart_btn)
        
        status_layout.addLayout(btn_layout)
        
        # Firewall Button
        self.firewall_btn = self.create_button("🛡️ باز کردن فایروال ویندوز", "#17a2b8", "#138496")
        status_layout.addWidget(self.firewall_btn)
        
        status_group.layout().addLayout(status_layout)
        content_layout.addWidget(status_group)
        
        # ==================== Settings Section ====================
        settings_group = self.create_group("🔧 تنظیمات")
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(12)
        
        # Host
        host_layout = QHBoxLayout()
        host_label = QLabel("🌐 میزبان:")
        host_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 100px;")
        host_layout.addWidget(host_label)
        
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("0.0.0.0")
        self.host_input.setStyleSheet(self.get_input_style())
        host_layout.addWidget(self.host_input, 1)
        settings_layout.addLayout(host_layout)
        
        # Port
        port_layout = QHBoxLayout()
        port_label = QLabel("🔌 پورت:")
        port_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 100px;")
        port_layout.addWidget(port_label)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(8080)
        self.port_input.setStyleSheet(self.get_input_style())
        self.port_input.setMinimumWidth(100)
        port_layout.addWidget(self.port_input)
        port_layout.addStretch()
        settings_layout.addLayout(port_layout)
        
        # Auto-start
        self.autostart_checkbox = QCheckBox("🚀 راه‌اندازی خودکار با اجرای برنامه")
        self.autostart_checkbox.setStyleSheet("font-size: 13px; font-weight: bold; padding: 8px 0;")
        settings_layout.addWidget(self.autostart_checkbox)
        
        # Token expiry
        token_layout = QHBoxLayout()
        token_label = QLabel("⏱️ اعتبار توکن:")
        token_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 100px;")
        token_layout.addWidget(token_label)
        
        self.token_expire_input = QSpinBox()
        self.token_expire_input.setRange(30, 1440)
        self.token_expire_input.setValue(480)
        self.token_expire_input.setSuffix(" دقیقه")
        self.token_expire_input.setStyleSheet(self.get_input_style())
        self.token_expire_input.setMinimumWidth(130)
        token_layout.addWidget(self.token_expire_input)
        token_layout.addStretch()
        settings_layout.addLayout(token_layout)
        
        settings_group.layout().addLayout(settings_layout)
        content_layout.addWidget(settings_group)
        
        # ==================== Info Section ====================
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #e7f3ff;
                border: 2px solid #007bff;
                border-radius: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(16, 14, 16, 14)
        
        info_text = """<div style="font-size: 12px; line-height: 1.8; color: #004085;">
<b>💡 راهنما:</b><br>
• برای دسترسی از گوشی، Host را <b>0.0.0.0</b> بگذارید<br>
• اگر از گوشی دسترسی ندارید، روی "باز کردن فایروال" بزنید<br>
• <b>ورود:</b> admin / admin123
</div>"""
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background: transparent; border: none;")
        info_layout.addWidget(info_label)
        
        content_layout.addWidget(info_frame)
        
        # Add stretch
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll, 1)
        
        # ==================== Bottom Buttons ====================
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet("background-color: white; border-top: 1px solid #ddd;")
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(20, 16, 20, 16)
        bottom_layout.setSpacing(12)
        
        self.save_btn = self.create_button("💾 ذخیره تنظیمات", "#007bff", "#0056b3")
        bottom_layout.addWidget(self.save_btn, 1)
        
        self.close_btn = self.create_button("❌ بستن", "#6c757d", "#5a6268")
        bottom_layout.addWidget(self.close_btn, 1)
        
        main_layout.addWidget(bottom_frame)
    
    def create_group(self, title):
        """Create a styled group box"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                border: 2px solid #ddd;
                border-radius: 10px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 8px;
                background-color: white;
            }
        """)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(12)
        return group
    
    def create_button(self, text, bg_color, hover_color):
        """Create a styled button"""
        btn = QPushButton(text)
        btn.setMinimumHeight(44)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
                padding: 0 16px;
            }}
            QPushButton:hover {{ background-color: {hover_color}; }}
            QPushButton:disabled {{ background-color: #ccc; color: #888; }}
        """)
        return btn
    
    def get_input_style(self):
        """Get style for input widgets"""
        return """
            font-size: 13px;
            padding: 10px 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background-color: white;
            min-height: 20px;
        """
    
    def get_url_label_style(self):
        """Get style for URL labels"""
        return """
            QLabel {
                font-size: 13px;
                color: #333;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 12px 14px;
            }
        """
    
    def update_status_style(self, is_running):
        """Update status label style"""
        if is_running:
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #155724;
                    background-color: #d4edda;
                    border: 2px solid #28a745;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
        else:
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #721c24;
                    background-color: #f8d7da;
                    border: 2px solid #dc3545;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
    
    def connect_signals(self):
        """Connect signals to slots"""
        self.start_btn.clicked.connect(self.start_server)
        self.stop_btn.clicked.connect(self.stop_server)
        self.restart_btn.clicked.connect(self.restart_server)
        self.save_btn.clicked.connect(self.save_settings)
        self.close_btn.clicked.connect(self.accept)
        self.firewall_btn.clicked.connect(self.open_firewall)
        
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
            QMessageBox.information(self, "✅ موفق", "تنظیمات ذخیره شد.\nبرای اعمال، سرور را ریستارت کنید.")
        except Exception as e:
            QMessageBox.critical(self, "❌ خطا", f"خطا در ذخیره:\n{str(e)}")
    
    def start_server(self):
        """Start the web server"""
        if self.server_runner.is_running:
            return
        self.start_btn.setEnabled(False)
        self.start_btn.setText("⏳ در حال راه‌اندازی...")
        self.server_runner.start()
    
    def stop_server(self):
        """Stop the web server"""
        if not self.server_runner.is_running:
            return
        self.stop_btn.setEnabled(False)
        self.stop_btn.setText("⏳ توقف...")
        self.server_runner.stop()
    
    def restart_server(self):
        """Restart the web server"""
        if not self.server_runner.is_running:
            self.start_server()
        else:
            self.restart_btn.setEnabled(False)
            self.restart_btn.setText("⏳ ریستارت...")
            self.server_runner.restart()
    
    def update_server_status(self):
        """Update server status display"""
        is_running = self.server_runner.is_running
        
        if is_running:
            self.status_label.setText("✅ سرور در حال اجراست")
            self.update_status_style(True)
            
            urls = self.server_runner.get_access_urls()
            self.url_label.setText(f"📍 آدرس محلی: {urls['local']}")
            self.url_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #155724;
                    background-color: #d4edda;
                    border: 1px solid #28a745;
                    border-radius: 8px;
                    padding: 12px 14px;
                }
            """)
            
            self.network_url_label.setText(f"🌐 آدرس شبکه: {urls['network']}")
            self.network_url_label.setStyleSheet("""
                QLabel {
                    font-size: 13px;
                    color: #155724;
                    background-color: #d4edda;
                    border: 1px solid #28a745;
                    border-radius: 8px;
                    padding: 12px 14px;
                }
            """)
            
            self.start_btn.setEnabled(False)
            self.start_btn.setText("▶️ راه‌اندازی")
            self.stop_btn.setEnabled(True)
            self.stop_btn.setText("⏹️ توقف")
            self.restart_btn.setEnabled(True)
            self.restart_btn.setText("🔄 ریستارت")
            
            # Show QR code
            self.update_qr_code()
        else:
            self.status_label.setText("⏹️ سرور متوقف است")
            self.update_status_style(False)
            
            self.url_label.setText("📍 آدرس محلی: -")
            self.url_label.setStyleSheet(self.get_url_label_style())
            
            self.network_url_label.setText("🌐 آدرس شبکه: -")
            self.network_url_label.setStyleSheet(self.get_url_label_style())
            
            self.start_btn.setEnabled(True)
            self.start_btn.setText("▶️ راه‌اندازی")
            self.stop_btn.setEnabled(False)
            self.stop_btn.setText("⏹️ توقف")
            self.restart_btn.setEnabled(False)
            self.restart_btn.setText("🔄 ریستارت")
            
            # Hide QR code
            self.qr_frame.setVisible(False)
    
    def on_server_started(self, host, port):
        """Called when server starts"""
        self.update_server_status()
        QMessageBox.information(
            self, "✅ سرور راه‌اندازی شد",
            f"آدرس: http://{host}:{port}\n\n"
            "برای دسترسی از گوشی، QR Code را اسکن کنید.\n"
            "اگر کار نکرد، روی 'باز کردن فایروال' بزنید."
        )
    
    def on_server_stopped(self):
        """Called when server stops"""
        self.update_server_status()
    
    def on_server_error(self, error):
        """Called when server error occurs"""
        self.update_server_status()
        QMessageBox.critical(self, "❌ خطا", f"خطای سرور:\n{error}")
    
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
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=2
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qimage = QImage()
            qimage.loadFromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)
            return pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print(f"QR Error: {e}")
            return None
    
    def update_qr_code(self):
        """Update QR code display"""
        if not self.server_runner.is_running or not HAS_QRCODE:
            self.qr_frame.setVisible(False)
            return
        
        urls = self.server_runner.get_access_urls()
        network_url = urls.get('network', '')
        
        if network_url and network_url != '-':
            pixmap = self.generate_qr_code(network_url)
            if pixmap:
                self.qr_label.setPixmap(pixmap)
                self.qr_frame.setVisible(True)
                return
        
        self.qr_frame.setVisible(False)
    
    def open_firewall(self):
        """Open Windows Firewall for the server port"""
        port = self.port_input.value()
        
        reply = QMessageBox.question(
            self, "🛡️ فایروال",
            f"پورت {port} در فایروال ویندوز باز شود؟\n\n"
            "نیاز به دسترسی Administrator دارد.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            import tempfile
            import os
            
            rule_name = f"CafeApp_Port_{port}"
            
            ps_script = f'''
$ruleName = "{rule_name}"
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if ($existingRule) {{
    Remove-NetFirewallRule -DisplayName $ruleName
}}
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow -Profile Any
Write-Host "Done! Port {port} is now open."
Write-Host ""
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
                f.write(ps_script)
                script_path = f.name
            
            command = f'powershell.exe -Command "Start-Process powershell.exe -Verb RunAs -ArgumentList \'-NoExit\', \'-File\', \'{script_path}\'"'
            
            subprocess.Popen(command, shell=True)
            
            QMessageBox.information(
                self, "✅ در حال اجرا",
                f"پنجره PowerShell با دسترسی Admin باید باز شود.\n\n"
                f"اگر پنجره UAC ظاهر شد، روی Yes بزنید.\n\n"
                f"اگر پنجره باز نشد، دستی اجرا کنید:\n"
                f"1. CMD را به عنوان Admin باز کنید\n"
                f"2. اجرا کنید:\n\n"
                f"netsh advfirewall firewall add rule name=\"CafeApp\" dir=in action=allow protocol=TCP localport={port}"
            )
            
        except Exception as e:
            QMessageBox.warning(
                self, "⚠️ خطا",
                f"خطا:\n{str(e)}\n\n"
                f"دستی اجرا کنید:\n"
                f"netsh advfirewall firewall add rule name=\"CafeApp\" dir=in action=allow protocol=TCP localport={port}"
            )
