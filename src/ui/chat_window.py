"""
Chat Window
Provides the main chat interface with message history and input.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading
from typing import Optional

class ChatWindow:
    def __init__(self, parent, controller, user_email: str):
        self.parent = parent
        self.controller = controller
        self.user_email = user_email
        self.is_typing = False
        
        # Add message callback to controller
        self.controller.add_message_callback(self.on_new_message)
        
        self.setup_ui()
        self.add_welcome_message()
        
    def setup_ui(self):
        """Setup the chat UI"""
        # Clear parent window
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Configure parent
        self.parent.title("AI Chat Assistant")
        
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.setup_header(main_frame)
        
        # Chat area
        self.setup_chat_area(main_frame)
        
        # Input area
        self.setup_input_area(main_frame)
        
        # Bind keyboard shortcuts
        self.parent.bind('<Control-m>', lambda e: self.minimize_to_tray())
        self.parent.bind('<F11>', lambda e: self.toggle_fullscreen())
    
    def setup_header(self, parent):
        """Setup the header with user info and controls"""
        header_frame = ttk.Frame(parent, style='Chat.TFrame', padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        header_frame.columnconfigure(1, weight=1)
        
        # AI Assistant info
        ai_info_frame = ttk.Frame(header_frame)
        ai_info_frame.grid(row=0, column=0, sticky=tk.W)
        
        # AI Avatar (using emoji)
        ttk.Label(ai_info_frame, text="🤖", font=('Segoe UI', 16)).grid(row=0, column=0, padx=(0, 10))
        
        ai_text_frame = ttk.Frame(ai_info_frame)
        ai_text_frame.grid(row=0, column=1)
        
        ttk.Label(ai_text_frame, text="AI Assistant", 
                 font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        
        self.status_label = ttk.Label(ai_text_frame, text="Online", 
                                     font=('Segoe UI', 9), foreground='green')
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # User info and controls
        user_frame = ttk.Frame(header_frame)
        user_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Message count
        self.message_count_label = ttk.Label(user_frame, text="0 messages", 
                                           font=('Segoe UI', 9), foreground='gray')
        self.message_count_label.grid(row=0, column=0, padx=(0, 10))
        
        # User email
        ttk.Label(user_frame, text=self.user_email, 
                 font=('Segoe UI', 9)).grid(row=0, column=1, padx=(0, 10))
        
        # Settings button
        settings_button = ttk.Button(user_frame, text="⚙️", width=3,
                                   command=self.show_settings)
        settings_button.grid(row=0, column=2, padx=(0, 5))
        
        # Minimize button
        minimize_button = ttk.Button(user_frame, text="−", width=3,
                                   command=self.minimize_to_tray)
        minimize_button.grid(row=0, column=3, padx=(0, 5))
        
        # Sign out button
        signout_button = ttk.Button(user_frame, text="Sign Out",
                                  command=self.handle_signout)
        signout_button.grid(row=0, column=4)
    
    def setup_chat_area(self, parent):
        """Setup the scrollable chat message area"""
        # Chat container with scrollbar
        chat_container = ttk.Frame(parent, style='Chat.TFrame')
        chat_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        chat_container.columnconfigure(0, weight=1)
        chat_container.rowconfigure(0, weight=1)
        
        # Create scrolled text widget for messages
        self.chat_text = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 10),
            bg='#ffffff',
            fg='#030213',
            padx=10,
            pady=10
        )
        self.chat_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for styling
        self.chat_text.tag_configure('user', 
                                    background='#030213', 
                                    foreground='#ffffff',
                                    relief='raised',
                                    borderwidth=1,
                                    wrap=tk.WORD,
                                    rmargin=100,
                                    justify='right')
        
        self.chat_text.tag_configure('ai', 
                                    background='#ececf0', 
                                    foreground='#030213',
                                    relief='raised',
                                    borderwidth=1,
                                    wrap=tk.WORD,
                                    lmargin1=0,
                                    lmargin2=0,
                                    rmargin=100)
        
        self.chat_text.tag_configure('timestamp', 
                                    font=('Segoe UI', 8), 
                                    foreground='gray')
        
        self.chat_text.tag_configure('typing', 
                                    font=('Segoe UI', 9), 
                                    foreground='gray',
                                    italic=True)
    
    def setup_input_area(self, parent):
        """Setup the message input area"""
        input_frame = ttk.Frame(parent, padding="10")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        # Input field and send button container
        input_container = ttk.Frame(input_frame)
        input_container.grid(row=0, column=0, sticky=(tk.W, tk.E))
        input_container.columnconfigure(0, weight=1)
        
        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(input_container, textvariable=self.message_var,
                                     font=('Segoe UI', 10))
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.message_entry.bind('<Return>', self.handle_send_message)
        self.message_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Send button
        self.send_button = ttk.Button(input_container, text="Send", 
                                    command=self.handle_send_message)
        self.send_button.grid(row=0, column=1)
        
        # Help text
        help_label = ttk.Label(input_frame, 
                              text="Press Enter to send • Ctrl+M to minimize to tray",
                              font=('Segoe UI', 8), foreground='gray')
        help_label.grid(row=1, column=0, pady=(5, 0))
        
        # Focus on input
        self.message_entry.focus()
    
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_text = "Hello! I'm your AI assistant. How can I help you today?"
        self.add_message_to_chat("🤖", welcome_text, "ai")
    
    def add_message_to_chat(self, sender: str, message: str, msg_type: str):
        """Add a message to the chat display"""
        self.chat_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        if msg_type == "user":
            # User message (right-aligned)
            self.chat_text.insert(tk.END, f"\n{sender} ({timestamp})\n", 'timestamp')
            self.chat_text.insert(tk.END, f"{message}\n", 'user')
        else:
            # AI message (left-aligned)
            self.chat_text.insert(tk.END, f"\n{sender} ({timestamp})\n", 'timestamp')
            self.chat_text.insert(tk.END, f"{message}\n", 'ai')
        
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
        # Update message count
        message_count = len(self.controller.get_message_history())
        self.message_count_label.config(text=f"{message_count} messages")
    
    def handle_send_message(self, event=None):
        """Handle sending a message"""
        message = self.message_var.get().strip()
        if not message or self.is_typing:
            return
        
        # Clear input
        self.message_var.set("")
        
        # Add user message to chat
        self.add_message_to_chat("You", message, "user")
        
        # Show typing indicator
        self.show_typing_indicator()
        
        # Send to AI
        self.controller.send_message_to_ai(message, self.on_ai_response)
    
    def on_ai_response(self, response: str):
        """Handle AI response"""
        # Hide typing indicator
        self.hide_typing_indicator()
        
        # Add AI response to chat
        self.add_message_to_chat("AI Assistant", response, "ai")
    
    def on_new_message(self, message):
        """Handle new message from controller"""
        # This is called when controller adds messages
        # We can use this for real-time updates if needed
        pass
    
    def show_typing_indicator(self):
        """Show AI typing indicator"""
        self.is_typing = True
        self.status_label.config(text="AI is typing...", foreground='blue')
        self.send_button.config(state='disabled')
        
        # Add typing dots to chat
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, "\nAI is typing", 'typing')
        self.typing_end = self.chat_text.index(tk.END + "-1c")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
        # Animate typing dots
        self.animate_typing_dots()
    
    def hide_typing_indicator(self):
        """Hide AI typing indicator"""
        self.is_typing = False
        self.status_label.config(text="Online", foreground='green')
        self.send_button.config(state='normal')
        
        # Remove typing indicator from chat
        if hasattr(self, 'typing_end'):
            self.chat_text.config(state=tk.NORMAL)
            # Find and remove the typing line
            try:
                # Get current content and remove last typing line
                content = self.chat_text.get("1.0", tk.END)
                lines = content.split('\n')
                if lines and 'typing' in lines[-2]:
                    # Remove the typing line
                    self.chat_text.delete("end-2l", "end-1l")
            except:
                pass
            self.chat_text.config(state=tk.DISABLED)
    
    def animate_typing_dots(self):
        """Animate typing dots"""
        if not self.is_typing:
            return
        
        try:
            self.chat_text.config(state=tk.NORMAL)
            # Update typing text with animated dots
            current_text = self.chat_text.get("end-2l", "end-1l").strip()
            if 'typing' in current_text:
                dots = len([c for c in current_text if c == '.'])
                new_dots = '.' * ((dots % 3) + 1)
                self.chat_text.delete("end-2l", "end-1l")
                self.chat_text.insert("end-1l", f"AI is typing{new_dots}\n", 'typing')
            self.chat_text.config(state=tk.DISABLED)
            
            # Schedule next animation
            self.parent.after(500, self.animate_typing_dots)
        except:
            pass
    
    def on_input_change(self, event=None):
        """Handle input field changes"""
        # Enable/disable send button based on input
        has_text = bool(self.message_var.get().strip())
        state = 'normal' if has_text and not self.is_typing else 'disabled'
        self.send_button.config(state=state)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.parent)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.parent)
        settings_window.grab_set()
        
        # Settings content
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Chat Settings", 
                 font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 20))
        
        # API Key setting
        ttk.Label(main_frame, text="AI API Key (Optional):").grid(row=1, column=0, sticky=tk.W)
        api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(main_frame, textvariable=api_key_var, width=50, show="*")
        api_key_entry.grid(row=2, column=0, pady=(5, 10), sticky=(tk.W, tk.E))
        
        # Clear chat button
        ttk.Button(main_frame, text="Clear Chat History", 
                  command=self.clear_chat).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        # About info
        ttk.Label(main_frame, text="AI Chat Desktop Application v1.0", 
                 font=('Segoe UI', 9)).grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        ttk.Label(main_frame, text="Built with Python and tkinter", 
                 font=('Segoe UI', 9), foreground='gray').grid(row=5, column=0, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
        def save_settings():
            api_key = api_key_var.get().strip()
            if api_key:
                self.controller.set_api_key(api_key)
                messagebox.showinfo("Settings", "API key saved successfully!")
            settings_window.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_settings).grid(row=0, column=0)
        ttk.Button(button_frame, text="Cancel", 
                  command=settings_window.destroy).grid(row=0, column=1, padx=(10, 0))
    
    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear all chat history?"):
            self.controller.clear_message_history()
            self.chat_text.config(state=tk.NORMAL)
            self.chat_text.delete("1.0", tk.END)
            self.chat_text.config(state=tk.DISABLED)
            self.add_welcome_message()
            self.message_count_label.config(text="0 messages")
    
    def minimize_to_tray(self):
        """Minimize window to system tray"""
        from main import AIChairApplication
        # Access the main app instance through parent
        if hasattr(self.parent, 'master') and hasattr(self.parent.master, 'minimize_to_tray'):
            self.parent.master.minimize_to_tray()
        else:
            # Fallback - just minimize window
            self.parent.withdraw()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.parent.attributes('-fullscreen')
        self.parent.attributes('-fullscreen', not current_state)
    
    def handle_signout(self):
        """Handle user sign out"""
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            # Clear chat history
            self.controller.clear_message_history()
            
            # Trigger sign out in main app
            # This would need to be connected to the main app
            messagebox.showinfo("Signed Out", "You have been signed out successfully.")
    
    def destroy(self):
        """Clean up the window"""
        # Remove message callback
        if self in self.controller.message_callbacks:
            self.controller.message_callbacks.remove(self.on_new_message)
        
        # Unbind events
        try:
            self.parent.unbind('<Control-m>')
            self.parent.unbind('<F11>')
        except:
            pass
        
        # Clear widgets
        for widget in self.parent.winfo_children():
            widget.destroy()