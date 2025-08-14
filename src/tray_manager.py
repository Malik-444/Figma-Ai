"""
System Tray Manager
Handles system tray integration for Windows and Mac.
"""

import sys
import threading
from pathlib import Path

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("Warning: pystray not available. Install with: pip install pystray Pillow")

class TrayManager:
    def __init__(self, app):
        self.app = app
        self.icon = None
        self.is_running = False
        self.unread_count = 0
        
        if TRAY_AVAILABLE:
            self.setup_icon()
    
    def setup_icon(self):
        """Setup the system tray icon"""
        # Create a simple colored circle icon
        image = self.create_icon_image()
        
        # Define the menu
        menu = pystray.Menu(
            item('Open Chat', self.restore_window, default=True),
            item('New Message', self.show_quick_message),
            pystray.Menu.SEPARATOR,
            item('Settings', self.show_settings),
            item('About', self.show_about),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_application)
        )
        
        # Create the icon
        self.icon = pystray.Icon(
            "AI Chat Assistant",
            image,
            "AI Chat Assistant",
            menu
        )
    
    def create_icon_image(self, color='blue'):
        """Create the tray icon image"""
        # Create a simple 64x64 icon
        width = 64
        height = 64
        
        # Create image
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw a circle
        margin = 8
        if color == 'blue':
            fill_color = (0, 123, 255, 255)  # Blue
        elif color == 'red':
            fill_color = (220, 53, 69, 255)   # Red for notifications
        else:
            fill_color = (108, 117, 125, 255)  # Gray
        
        draw.ellipse([margin, margin, width-margin, height-margin], 
                    fill=fill_color, outline=(255, 255, 255, 255), width=2)
        
        # Add chat bubble indicator
        draw.ellipse([width-24, height-24, width-8, height-8], 
                    fill=(255, 255, 255, 255))
        
        # Add unread count if any
        if self.unread_count > 0:
            # Draw red notification badge
            badge_size = 20
            badge_x = width - badge_size - 2
            badge_y = 2
            
            draw.ellipse([badge_x, badge_y, badge_x + badge_size, badge_y + badge_size],
                        fill=(220, 53, 69, 255))
            
            # Add count text (simplified for small numbers)
            count_text = str(min(self.unread_count, 9)) if self.unread_count < 10 else "9+"
            # Note: For proper text rendering, you'd want to use a font
            # This is a simplified version
        
        return image
    
    def start(self):
        """Start the tray icon"""
        if not TRAY_AVAILABLE or self.is_running:
            return
        
        self.is_running = True
        
        try:
            # Run the icon (this blocks)
            if self.icon:
                self.icon.run()
        except Exception as e:
            print(f"Tray manager error: {e}")
            self.is_running = False
    
    def stop(self):
        """Stop the tray icon"""
        if not TRAY_AVAILABLE or not self.is_running:
            return
        
        self.is_running = False
        
        if self.icon:
            self.icon.stop()
    
    def update_unread_count(self, count: int):
        """Update unread message count"""
        self.unread_count = count
        
        if self.icon and self.is_running:
            # Update icon with new count
            new_image = self.create_icon_image('red' if count > 0 else 'blue')
            self.icon.icon = new_image
    
    def show_notification(self, title: str, message: str = None):
        """Show system notification"""
        if not TRAY_AVAILABLE:
            print(f"Notification: {title} - {message}")
            return
        
        try:
            if self.icon:
                self.icon.notify(message or title, title)
        except Exception as e:
            print(f"Notification error: {e}")
    
    def restore_window(self, icon=None, item=None):
        """Restore the main window"""
        if self.app:
            self.app.restore_from_tray()
    
    def show_quick_message(self, icon=None, item=None):
        """Show quick message dialog"""
        # This would open a small popup for quick messages
        self.restore_window()
        self.show_notification("Quick Message", "Feature coming soon!")
    
    def show_settings(self, icon=None, item=None):
        """Show settings"""
        self.restore_window()
        # Focus on settings - would need to communicate with main app
    
    def show_about(self, icon=None, item=None):
        """Show about dialog"""
        self.show_notification("AI Chat Assistant", 
                             "Python desktop application with AI chat capabilities")
    
    def quit_application(self, icon=None, item=None):
        """Quit the entire application"""
        if self.app:
            self.app.quit_application()

class MockTrayManager:
    """Mock tray manager for when pystray is not available"""
    
    def __init__(self, app):
        self.app = app
        self.unread_count = 0
        print("Mock tray manager initialized (pystray not available)")
    
    def start(self):
        print("Mock tray: Started")
    
    def stop(self):
        print("Mock tray: Stopped")
    
    def update_unread_count(self, count: int):
        self.unread_count = count
        print(f"Mock tray: Unread count updated to {count}")
    
    def show_notification(self, title: str, message: str = None):
        print(f"Mock notification: {title} - {message}")

# Use mock if pystray not available
if not TRAY_AVAILABLE:
    TrayManager = MockTrayManager