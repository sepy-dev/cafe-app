# web/config.py - Web Server Configuration
import json
import os
from dataclasses import dataclass, asdict
from typing import Optional
import secrets


@dataclass
class ServerConfig:
    """Web server configuration"""
    host: str = "0.0.0.0"  # Listen on all interfaces for network access
    port: int = 8080
    enabled: bool = False
    auto_start: bool = False
    secret_key: str = ""
    token_expire_minutes: int = 480  # 8 hours
    allow_registration: bool = False  # Only admin can create users by default
    
    def __post_init__(self):
        if not self.secret_key:
            self.secret_key = secrets.token_hex(32)


class ServerConfigManager:
    """Manages server configuration persistence"""
    
    CONFIG_FILE = "server_config.json"
    
    def __init__(self, config_dir: str = "Config"):
        self.config_dir = config_dir
        self.config_path = os.path.join(config_dir, self.CONFIG_FILE)
        self._config: Optional[ServerConfig] = None
    
    @property
    def config(self) -> ServerConfig:
        if self._config is None:
            self._config = self.load()
        return self._config
    
    def load(self) -> ServerConfig:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return ServerConfig(**data)
        except Exception as e:
            print(f"Error loading server config: {e}")
        
        # Return default config
        config = ServerConfig()
        self.save(config)
        return config
    
    def save(self, config: ServerConfig) -> bool:
        """Save configuration to file"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)
            self._config = config
            return True
        except Exception as e:
            print(f"Error saving server config: {e}")
            return False
    
    def update(self, **kwargs) -> ServerConfig:
        """Update configuration with new values"""
        config = self.config
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        self.save(config)
        return config


# Global instance
_config_manager: Optional[ServerConfigManager] = None


def get_config_manager() -> ServerConfigManager:
    global _config_manager
    if _config_manager is None:
        _config_manager = ServerConfigManager()
    return _config_manager

