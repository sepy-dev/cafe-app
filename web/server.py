# web/server.py - Web Server Runner
import threading
import socket
import asyncio
from typing import Optional, Callable
import uvicorn
from PySide6.QtCore import QObject, Signal

from web.config import get_config_manager, ServerConfig


class ServerRunner(QObject):
    """Web server runner that manages the Uvicorn server in a separate thread"""
    
    # Signals
    server_started = Signal(str, int)  # host, port
    server_stopped = Signal()
    server_error = Signal(str)
    status_changed = Signal(str)  # status message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._server: Optional[uvicorn.Server] = None
        self._thread: Optional[threading.Thread] = None
        self._is_running = False
        self._config_manager = get_config_manager()
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @property
    def config(self) -> ServerConfig:
        return self._config_manager.config
    
    def get_local_ip(self) -> str:
        """Get the local IP address for network access"""
        try:
            # Create a socket to determine the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def start(self) -> bool:
        """Start the web server"""
        if self._is_running:
            self.server_error.emit("سرور در حال اجرا است")
            return False
        
        try:
            config = self.config
            
            # Create Uvicorn config
            uvicorn_config = uvicorn.Config(
                "web.api:app",
                host=config.host,
                port=config.port,
                log_level="info",
                reload=False,
                access_log=True
            )
            
            self._server = uvicorn.Server(uvicorn_config)
            
            # Start server in a separate thread
            self._thread = threading.Thread(target=self._run_server, daemon=True)
            self._thread.start()
            
            self._is_running = True
            local_ip = self.get_local_ip()
            self.server_started.emit(local_ip, config.port)
            self.status_changed.emit(f"سرور روشن شد: http://{local_ip}:{config.port}")
            
            return True
            
        except Exception as e:
            self.server_error.emit(f"خطا در راه‌اندازی سرور: {str(e)}")
            return False
    
    def _run_server(self):
        """Run the server (called in a separate thread)"""
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._server.serve())
        except Exception as e:
            self.server_error.emit(f"خطای سرور: {str(e)}")
        finally:
            self._is_running = False
            self.server_stopped.emit()
    
    def stop(self) -> bool:
        """Stop the web server"""
        if not self._is_running or not self._server:
            return False
        
        try:
            self._server.should_exit = True
            self._is_running = False
            self.status_changed.emit("سرور متوقف شد")
            self.server_stopped.emit()
            return True
        except Exception as e:
            self.server_error.emit(f"خطا در توقف سرور: {str(e)}")
            return False
    
    def restart(self) -> bool:
        """Restart the web server"""
        self.stop()
        # Wait a moment for the server to fully stop
        import time
        time.sleep(0.5)
        return self.start()
    
    def update_config(self, **kwargs) -> ServerConfig:
        """Update server configuration"""
        return self._config_manager.update(**kwargs)
    
    def get_access_urls(self) -> dict:
        """Get the URLs to access the server"""
        config = self.config
        local_ip = self.get_local_ip()
        
        return {
            "local": f"http://127.0.0.1:{config.port}",
            "network": f"http://{local_ip}:{config.port}",
            "host": config.host,
            "port": config.port
        }


# Global server instance
_server_runner: Optional[ServerRunner] = None


def get_server_runner() -> ServerRunner:
    """Get the global server runner instance"""
    global _server_runner
    if _server_runner is None:
        _server_runner = ServerRunner()
    return _server_runner

