#!/usr/bin/env python3
"""
AI Chat Desktop Application
A Python desktop application with authentication, AI chat, and system tray functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.app_controller import AppController
from src.ui.auth_window import AuthWindow
from src.ui.chat_window import ChatWindow
from src.tray_manager import TrayManager
from src.config import Config

class AIChairApplication:
    def __init__(self):
        self.config = Config()
        self.root = None
        self.current_window = None
        self.tray_manager = None
        self.controller = AppController()
        self.is_authenticated = False
        self.user_email = None
        
    def initialize(self):
        """Initialize the application"""
        # Setup tkinter root window
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially
        
        # Configure root window
        self.root.title("AI Chat Assistant")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        try:
            if os.path.exists("assets/icon.ico"):
                self.root.iconbitmap("assets/icon.ico")
        except:
            pass
            
        # Apply theme
        self.setup_theme()
        
        # Initialize tray manager
        self.tray_manager = TrayManager(self)
        
        # Show authentication window
        self.show_auth_window()
        
    def setup_theme(self):
        """Setup application theme matching the original design"""
        style = ttk.Style()
        
        # Configure colors to match the original design
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#030213')
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#717182')
        
        style.configure('Chat.TFrame',
                       background='#ffffff',
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Message.TLabel',
                       font=('Segoe UI', 9),
                       wraplength=400)
        
        style.configure('UserMessage.TLabel',
                       font=('Segoe UI', 9),
                       background='#030213',
                       foreground='#ffffff',
                       wraplength=400)
        
        style.configure('AIMessage.TLabel',
                       font=('Segoe UI', 9),
                       background='#ececf0',
                       foreground='#030213',
                       wraplength=400)
    
    def show_auth_window(self):
        """Show the authentication window"""
        if self.current_window:
            self.current_window.destroy()
            
        self.current_window = AuthWindow(self.root, self.controller, self.on_authentication_success)
        self.root.deiconify()  # Show window
        
    def show_chat_window(self):
        """Show the chat window"""
        if self.current_window:
            self.current_window.destroy()
            
        self.current_window = ChatWindow(self.root, self.controller, self.user_email)
        self.root.deiconify()  # Show window
        
    def on_authentication_success(self, email):
        """Handle successful authentication"""
        self.is_authenticated = True
        self.user_email = email
        self.show_chat_window()
        
        # Start tray manager
        if self.tray_manager:
            threading.Thread(target=self.tray_manager.start, daemon=True).start()
    
    def on_sign_out(self):
        """Handle user sign out"""
        self.is_authenticated = False
        self.user_email = None
        self.show_auth_window()
        
        # Stop tray if running
        if self.tray_manager:
            self.tray_manager.stop()
    
    def minimize_to_tray(self):
        """Minimize application to system tray"""
        self.root.withdraw()
        if self.tray_manager:
            self.tray_manager.show_notification("AI Chat minimized to tray")
    
    def restore_from_tray(self):
        """Restore application from system tray"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def quit_application(self):
        """Quit the application"""
        if self.tray_manager:
            self.tray_manager.stop()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Run the application"""
        try:
            self.initialize()
            
            # Handle window close event
            self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
            
            # Start the main loop
            self.root.mainloop()
            
        except KeyboardInterrupt:
            self.quit_application()
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")
            self.quit_application()

if __name__ == "__main__":
    app = AIChairApplication()
    app.run()