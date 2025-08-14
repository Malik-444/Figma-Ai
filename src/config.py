"""
Configuration Management
Handles application settings and configuration.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".ai_chat_app"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "app": {
                "name": "AI Chat Assistant",
                "version": "1.0.0",
                "window_width": 800,
                "window_height": 600,
                "theme": "light"
            },
            "auth": {
                "remember_email": True,
                "auto_signin": False,
                "session_timeout": 3600  # 1 hour
            },
            "chat": {
                "max_history": 1000,
                "auto_scroll": True,
                "show_timestamps": True,
                "notification_sound": True
            },
            "ai": {
                "api_provider": "mock",  # "openai", "anthropic", "mock"
                "api_key": "",
                "model": "gpt-3.5-turbo",
                "max_tokens": 500,
                "temperature": 0.7
            },
            "tray": {
                "minimize_to_tray": True,
                "close_to_tray": True,
                "show_notifications": True,
                "notification_duration": 5
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                
                # Merge with defaults (add any missing keys)
                config = self.default_config.copy()
                self._deep_update(config, loaded_config)
                return config
            else:
                # Create config directory and return defaults
                self.config_dir.mkdir(exist_ok=True)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'app.name')"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config_section = self.config
        
        try:
            # Navigate to the parent section
            for key in keys[:-1]:
                if key not in config_section:
                    config_section[key] = {}
                config_section = config_section[key]
            
            # Set the value
            config_section[keys[-1]] = value
            
            # Auto-save
            return self.save_config()
            
        except Exception as e:
            print(f"Error setting config value: {e}")
            return False
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    # Convenience methods for common settings
    
    @property
    def window_size(self) -> tuple:
        """Get window size as (width, height)"""
        return (self.get('app.window_width', 800), self.get('app.window_height', 600))
    
    @window_size.setter
    def window_size(self, size: tuple):
        """Set window size"""
        width, height = size
        self.set('app.window_width', width)
        self.set('app.window_height', height)
    
    @property
    def api_key(self) -> str:
        """Get AI API key"""
        return self.get('ai.api_key', '')
    
    @api_key.setter
    def api_key(self, key: str):
        """Set AI API key"""
        self.set('ai.api_key', key)
    
    @property
    def theme(self) -> str:
        """Get application theme"""
        return self.get('app.theme', 'light')
    
    @theme.setter
    def theme(self, theme: str):
        """Set application theme"""
        self.set('app.theme', theme)
    
    @property
    def minimize_to_tray(self) -> bool:
        """Get minimize to tray setting"""
        return self.get('tray.minimize_to_tray', True)
    
    @minimize_to_tray.setter
    def minimize_to_tray(self, value: bool):
        """Set minimize to tray setting"""
        self.set('tray.minimize_to_tray', value)