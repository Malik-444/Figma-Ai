"""
AI Chat Desktop Application
A Python desktop application with AI chat capabilities and system tray integration.
"""

__version__ = "1.0.0"
__author__ = "AI Chat Team"
__description__ = "Desktop AI Chat Assistant with Authentication and Tray Integration"

from .config import Config
from .app_controller import AppController

__all__ = ['Config', 'AppController']