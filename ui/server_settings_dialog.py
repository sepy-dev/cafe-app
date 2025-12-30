# ui/server_settings_dialog.py
"""
Server Settings Dialog for managing the web server configuration
"""
import subprocess
import io
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QSpinBox, QCheckBox,
    QMessageBox, QFrame, QWidget
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
        self.setFixedSize(750, 850)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        self.setup_ui()
        self.load_settings()
        self.connect_signals()
        self.update_server_status()
    
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ==================== Server Status Section ====================
        status_group = QGroupBox("📊 وضعیت سرور")
        status_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """)
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(15)
        status_layout.setContentsMargins(15, 25, 15, 15)
        
        # Status Label
        self.status_label = QLabel("⏹️ سرور متوقف است")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMinimumHeight(50)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #dc3545;
                background-color: #f8d7da;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        # URL Labels
        url_frame = QFrame()
        url_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 10px;")
        url_layout = QVBoxLayout(url_frame)
        url_layout.setSpacing(10)
        url_layout.setContentsMargins(15, 15, 15, 15)
        
        self.url_label = QLabel("📍 آدرس محلی: -")
        self.url_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px 15px;
            }
        """)
        self.url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        url_layout.addWidget(self.url_label)
        
        self.network_url_label = QLabel("🌐 آدرس شبکه: -")
        self.network_url_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px 15px;
            }
        """)
        self.network_url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        url_layout.addWidget(self.network_url_label)
        
        status_layout.addWidget(url_frame)
        
        # QR Code
        self.qr_frame = QFrame()
        self.qr_frame.setStyleSheet("background-color: white; border-radius: 8px;")
        self.qr_frame.setVisible(False)
        qr_layout = QVBoxLayout(self.qr_frame)
        qr_layout.setContentsMargins(15, 15, 15, 15)
        qr_layout.setSpacing(10)
        
        qr_title = QLabel("📱 اسکن با گوشی:")
        qr_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #333; background: transparent;")
        qr_title.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(qr_title)
        
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumSize(180, 180)
        self.qr_label.setMaximumSize(180, 180)
        self.qr_label.setStyleSheet("background-color: white; border: 2px solid #ddd; border-radius: 8px;")
        qr_layout.addWidget(self.qr_label, 0, Qt.AlignCenter)
        
        status_layout.addWidget(self.qr_frame)
        
        # Control Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.start_btn = QPushButton("▶️ راه‌اندازی")
        self.start_btn.setMinimumHeight(45)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #218838; }
            QPushButton:disabled { background-color: #aaa; }
        """)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ توقف")
        self.stop_btn.setMinimumHeight(45)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #c82333; }
            QPushButton:disabled { background-color: #aaa; }
        """)
        btn_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("🔄 راه‌اندازی مجدد")
        self.restart_btn.setMinimumHeight(45)
        self.restart_btn.setCursor(Qt.PointingHandCursor)
        self.restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #e96b02; }
            QPushButton:disabled { background-color: #aaa; }
        """)
        btn_layout.addWidget(self.restart_btn)
        
        status_layout.addLayout(btn_layout)
        
        # Firewall Button
        self.firewall_btn = QPushButton("🛡️ باز کردن فایروال (برای دسترسی از شبکه)")
        self.firewall_btn.setMinimumHeight(45)
        self.firewall_btn.setCursor(Qt.PointingHandCursor)
        self.firewall_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #138496; }
        """)
        status_layout.addWidget(self.firewall_btn)
        
        main_layout.addWidget(status_group)
        
        # ==================== Settings Section ====================
        settings_group = QGroupBox("🔧 تنظیمات")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
        """)
        settings_layout = QVBoxLayout(settings_group)
        settings_layout.setSpacing(15)
        settings_layout.setContentsMargins(15, 25, 15, 15)
        
        # Host
        host_row = QHBoxLayout()
        host_label = QLabel("🌐 آدرس میزبان:")
        host_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 140px;")
        host_row.addWidget(host_label)
        
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("0.0.0.0 برای دسترسی از شبکه")
        self.host_input.setMinimumHeight(40)
        self.host_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus { border-color: #007bff; }
        """)
        host_row.addWidget(self.host_input, 1)
        settings_layout.addLayout(host_row)
        
        # Port
        port_row = QHBoxLayout()
        port_label = QLabel("🔌 پورت:")
        port_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 140px;")
        port_row.addWidget(port_label)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(8080)
        self.port_input.setMinimumHeight(40)
        self.port_input.setMinimumWidth(120)
        self.port_input.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QSpinBox:focus { border-color: #007bff; }
        """)
        port_row.addWidget(self.port_input)
        port_row.addStretch()
        settings_layout.addLayout(port_row)
        
        # Auto-start
        autostart_row = QHBoxLayout()
        autostart_label = QLabel("🚀 راه‌اندازی خودکار:")
        autostart_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 140px;")
        autostart_row.addWidget(autostart_label)
        
        self.autostart_checkbox = QCheckBox("راه‌اندازی خودکار با اجرای برنامه")
        self.autostart_checkbox.setStyleSheet("font-size: 13px;")
        autostart_row.addWidget(self.autostart_checkbox)
        autostart_row.addStretch()
        settings_layout.addLayout(autostart_row)
        
        # Token expiry
        token_row = QHBoxLayout()
        token_label = QLabel("⏱️ اعتبار توکن:")
        token_label.setStyleSheet("font-size: 13px; font-weight: bold; min-width: 140px;")
        token_row.addWidget(token_label)
        
        self.token_expire_input = QSpinBox()
        self.token_expire_input.setRange(30, 1440)
        self.token_expire_input.setValue(480)
        self.token_expire_input.setSuffix(" دقیقه")
        self.token_expire_input.setMinimumHeight(40)
        self.token_expire_input.setMinimumWidth(140)
        self.token_expire_input.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QSpinBox:focus { border-color: #007bff; }
        """)
        token_row.addWidget(self.token_expire_input)
        token_row.addStretch()
        settings_layout.addLayout(token_row)
        
        main_layout.addWidget(settings_group)
        
        # ==================== Info Section ====================
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        
        info_label = QLabel("""
<div style="font-size: 12px; line-height: 1.6;">
<b>📌 راهنما:</b><br>
• برای دسترسی از شبکه، ابتدا روی "باز کردن فایروال" کلیک کنید<br>
• آدرس Host را روی <b>0.0.0.0</b> تنظیم کنید<br>
• <b>کاربر پیش‌فرض:</b> admin / admin123
</div>
        """)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background: transparent; color: #856404;")
        info_layout.addWidget(info_label)
        
        main_layout.addWidget(info_frame)
        
        # ==================== Bottom Buttons ====================
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)
        
        self.save_btn = QPushButton("💾 ذخیره تنظیمات")
        self.save_btn.setMinimumHeight(50)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #0056b3; }
        """)
        bottom_layout.addWidget(self.save_btn, 1)
        
        self.close_btn = QPushButton("❌ بستن")
        self.close_btn.setMinimumHeight(50)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        bottom_layout.addWidget(self.close_btn, 1)
        
        main_layout.addLayout(bottom_layout)
    
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
            QMessageBox.information(self, "✅ موفق", "تنظیمات ذخیره شد.\nبرای اعمال، سرور را مجدداً راه‌اندازی کنید.")
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
        self.stop_btn.setText("⏳ در حال توقف...")
        self.server_runner.stop()
    
    def restart_server(self):
        """Restart the web server"""
        if not self.server_runner.is_running:
            self.start_server()
        else:
            self.restart_btn.setEnabled(False)
            self.restart_btn.setText("⏳ در حال راه‌اندازی...")
            self.server_runner.restart()
    
    def update_server_status(self):
        """Update server status display"""
        if self.server_runner.is_running:
            self.status_label.setText("✅ سرور در حال اجراست")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #155724;
                    background-color: #d4edda;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
            
            urls = self.server_runner.get_access_urls()
            self.url_label.setText(f"📍 آدرس محلی: {urls['local']}")
            self.url_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #155724;
                    background-color: #c3e6cb;
                    border: 1px solid #28a745;
                    border-radius: 5px;
                    padding: 10px 15px;
                }
            """)
            
            self.network_url_label.setText(f"🌐 آدرس شبکه: {urls['network']}")
            self.network_url_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #155724;
                    background-color: #c3e6cb;
                    border: 1px solid #28a745;
                    border-radius: 5px;
                    padding: 10px 15px;
                }
            """)
            
            self.start_btn.setEnabled(False)
            self.start_btn.setText("▶️ راه‌اندازی")
            self.stop_btn.setEnabled(True)
            self.stop_btn.setText("⏹️ توقف")
            self.restart_btn.setEnabled(True)
            self.restart_btn.setText("🔄 راه‌اندازی مجدد")
            
            # Show QR code
            self.update_qr_code()
        else:
            self.status_label.setText("⏹️ سرور متوقف است")
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #721c24;
                    background-color: #f8d7da;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
            
            self.url_label.setText("📍 آدرس محلی: -")
            self.url_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #333;
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px 15px;
                }
            """)
            
            self.network_url_label.setText("🌐 آدرس شبکه: -")
            self.network_url_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #333;
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px 15px;
                }
            """)
            
            self.start_btn.setEnabled(True)
            self.start_btn.setText("▶️ راه‌اندازی")
            self.stop_btn.setEnabled(False)
            self.stop_btn.setText("⏹️ توقف")
            self.restart_btn.setEnabled(False)
            self.restart_btn.setText("🔄 راه‌اندازی مجدد")
            
            # Hide QR code
            self.qr_frame.setVisible(False)
    
    def on_server_started(self, host, port):
        """Called when server starts"""
        self.update_server_status()
        QMessageBox.information(
            self, "✅ سرور راه‌اندازی شد",
            f"آدرس محلی: http://127.0.0.1:{port}\n"
            f"آدرس شبکه: http://{host}:{port}\n\n"
            "اگر از گوشی دسترسی ندارید، روی 'باز کردن فایروال' کلیک کنید."
        )
    
    def on_server_stopped(self):
        """Called when server stops"""
        self.update_server_status()
    
    def on_server_error(self, error):
        """Called when server error occurs"""
        self.update_server_status()
        QMessageBox.critical(self, "❌ خطای سرور", f"خطا:\n{error}")
    
    def on_status_changed(self, status):
        """Called when server status changes"""
        self.update_server_status()
    
    def generate_qr_code(self, url):
        """Generate QR code for the URL"""
        if not HAS_QRCODE:
            return None
        try:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qimage = QImage()
            qimage.loadFromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimage)
            return pixmap.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        
        if network_url:
            pixmap = self.generate_qr_code(network_url)
            if pixmap:
                self.qr_label.setPixmap(pixmap)
                self.qr_frame.setVisible(True)
                return
        
        self.qr_frame.setVisible(False)
    
    def open_firewall(self):
        """Open Windows Firewall for the server port (requires Admin)"""
        port = self.port_input.value()
        
        reply = QMessageBox.question(
            self, "🛡️ باز کردن فایروال",
            f"آیا می‌خواهید پورت {port} را در فایروال ویندوز باز کنید؟\n\n"
            "این عملیات نیاز به دسترسی Administrator دارد.\n"
            "پس از تأیید، یک پنجره UAC ظاهر می‌شود که باید تأیید کنید.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                rule_name = f"CafeApp_Port_{port}"
                
                # Create a temporary PowerShell script file
                import tempfile
                import os
                
                ps_script_content = f'''
$ruleName = "{rule_name}"
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if ($existingRule) {{
    Remove-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
    Write-Host "Existing rule removed"
}}
try {{
    New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow -Profile Any
    Write-Host "Firewall rule created successfully!"
    Write-Host "Port {port} is now open in Windows Firewall"
}} catch {{
    Write-Host "Error: $_"
    Write-Host "Please check if you have administrator privileges"
}}
Write-Host ""
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'''
                
                # Write script to temp file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
                    f.write(ps_script_content)
                    script_path = f.name
                
                try:
                    # Method 1: Try using subprocess.run with shell=True
                    # Escape the script path properly for PowerShell
                    script_path_escaped = script_path.replace('\\', '\\\\')
                    
                    # Use Start-Process with -File parameter
                    ps_cmd = [
                        'powershell.exe',
                        '-Command',
                        f'Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoExit", "-File", "{script_path}"'
                    ]
                    
                    # Execute
                    process = subprocess.Popen(
                        ps_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    )
                    
                    # Give it a moment to start
                    import time
                    time.sleep(0.5)
                    
                    QMessageBox.information(
                        self,
                        "✅ پنجره Admin باز شد",
                        f"پنجره PowerShell با دسترسی Administrator باید باز شده باشد.\n\n"
                        f"در پنجره PowerShell:\n"
                        f"- اگر پیام 'Firewall rule created successfully!' دیدید، پورت {port} باز شده است.\n"
                        f"- اگر خطا دیدید، دستورات دستی را در پایین ببینید.\n\n"
                        f"اگر پنجره باز نشد، دستی انجام دهید:\n"
                        f"1. Command Prompt را به عنوان Admin باز کنید\n"
                        f"2. دستور زیر را اجرا کنید:\n\n"
                        f"netsh advfirewall firewall add rule name=\"CafeApp\" dir=in action=allow protocol=TCP localport={port}"
                    )
                    
                except Exception as e:
                    # Clean up temp file
                    try:
                        os.unlink(script_path)
                    except:
                        pass
                    
                    # Show manual instructions
                    QMessageBox.warning(
                        self,
                        "⚠️ خطا",
                        f"خطا در اجرای خودکار:\n{str(e)}\n\n"
                        f"لطفاً دستی انجام دهید:\n\n"
                        f"1. Command Prompt را به عنوان Administrator باز کنید\n"
                        f"2. دستور زیر را اجرا کنید:\n\n"
                        f"netsh advfirewall firewall add rule name=\"CafeApp\" dir=in action=allow protocol=TCP localport={port}"
                    )
                
            except Exception as e:
                # Show manual instructions if automatic method fails
                QMessageBox.warning(
                    self,
                    "⚠️ خطا",
                    f"خطا در اجرای خودکار:\n{str(e)}\n\n"
                    f"لطفاً دستی انجام دهید:\n\n"
                    f"1. Command Prompt را به عنوان Administrator باز کنید\n"
                    f"2. دستور زیر را اجرا کنید:\n\n"
                    f"netsh advfirewall firewall add rule name=\"CafeApp\" dir=in action=allow protocol=TCP localport={port}"
                )
