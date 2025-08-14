"""
Authentication Window
Provides login interface with email/password and Microsoft SSO options.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import Callable

class AuthWindow:
    def __init__(self, parent, controller, success_callback: Callable[[str], None]):
        self.parent = parent
        self.controller = controller
        self.success_callback = success_callback
        self.is_loading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the authentication UI"""
        # Clear parent window
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = ttk.Frame(self.parent, padding="40")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure parent grid
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Welcome back", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame, 
            text="Sign in to your account to continue",
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Microsoft SSO Button
        self.microsoft_button = ttk.Button(
            main_frame,
            text="🟢 Continue with Microsoft",
            command=self.handle_microsoft_auth,
            width=40
        )
        self.microsoft_button.grid(row=2, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Separator
        separator_frame = ttk.Frame(main_frame)
        separator_frame.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        separator_frame.columnconfigure(0, weight=1)
        separator_frame.columnconfigure(2, weight=1)
        
        ttk.Separator(separator_frame, orient='horizontal').grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Label(separator_frame, text="Or continue with email", 
                 style='Subtitle.TLabel').grid(row=0, column=1, padx=10)
        ttk.Separator(separator_frame, orient='horizontal').grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        # Email field
        ttk.Label(main_frame, text="Email").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=40)
        self.email_entry.grid(row=5, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        self.email_entry.insert(0, "demo@example.com")  # Demo placeholder
        
        # Password field
        ttk.Label(main_frame, text="Password").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                       show="*", width=40)
        self.password_entry.grid(row=7, column=0, pady=(0, 15), sticky=(tk.W, tk.E))
        self.password_entry.insert(0, "password123")  # Demo placeholder
        
        # Remember me and forgot password
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=8, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        options_frame.columnconfigure(1, weight=1)
        
        self.remember_var = tk.BooleanVar()
        remember_check = ttk.Checkbutton(options_frame, text="Remember me", 
                                        variable=self.remember_var)
        remember_check.grid(row=0, column=0, sticky=tk.W)
        
        forgot_button = ttk.Button(options_frame, text="Forgot password?", 
                                  command=self.handle_forgot_password)
        forgot_button.grid(row=0, column=1, sticky=tk.E)
        
        # Sign in button
        self.signin_button = ttk.Button(
            main_frame,
            text="Sign in",
            command=self.handle_email_auth,
            width=40
        )
        self.signin_button.grid(row=9, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Sign up link
        signup_frame = ttk.Frame(main_frame)
        signup_frame.grid(row=10, column=0)
        
        ttk.Label(signup_frame, text="Don't have an account?", 
                 style='Subtitle.TLabel').grid(row=0, column=0)
        ttk.Button(signup_frame, text="Sign up", 
                  command=self.handle_signup).grid(row=0, column=1, padx=(5, 0))
        
        # Status label for loading/errors
        self.status_label = ttk.Label(main_frame, text="", foreground='red')
        self.status_label.grid(row=11, column=0, pady=(10, 0))
        
        # Bind Enter key to sign in
        self.parent.bind('<Return>', lambda e: self.handle_email_auth())
        
        # Focus on email field
        self.email_entry.focus()
    
    def handle_email_auth(self):
        """Handle email/password authentication"""
        if self.is_loading:
            return
            
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        
        if not email or not password:
            self.show_error("Please enter both email and password")
            return
        
        self.set_loading(True, "Signing in...")
        
        def auth_thread():
            try:
                success = self.controller.authenticate_email(email, password)
                
                # Update UI in main thread
                self.parent.after(0, lambda: self.handle_auth_result(success, email))
                
            except Exception as e:
                self.parent.after(0, lambda: self.handle_auth_error(str(e)))
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def handle_microsoft_auth(self):
        """Handle Microsoft SSO authentication"""
        if self.is_loading:
            return
            
        self.set_loading(True, "Authenticating with Microsoft...")
        
        def auth_thread():
            try:
                email = self.controller.authenticate_microsoft()
                
                # Update UI in main thread
                self.parent.after(0, lambda: self.handle_auth_result(bool(email), email))
                
            except Exception as e:
                self.parent.after(0, lambda: self.handle_auth_error(str(e)))
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def handle_auth_result(self, success: bool, email: str = None):
        """Handle authentication result"""
        self.set_loading(False)
        
        if success and email:
            self.success_callback(email)
        else:
            self.show_error("Invalid email or password. Try demo@example.com / password123")
    
    def handle_auth_error(self, error: str):
        """Handle authentication error"""
        self.set_loading(False)
        self.show_error(f"Authentication error: {error}")
    
    def handle_forgot_password(self):
        """Handle forgot password"""
        messagebox.showinfo("Forgot Password", 
                           "Password reset functionality would be implemented here.\n"
                           "For demo, use: demo@example.com / password123")
    
    def handle_signup(self):
        """Handle sign up"""
        messagebox.showinfo("Sign Up", 
                           "Sign up functionality would be implemented here.\n"
                           "For demo, use: demo@example.com / password123")
    
    def set_loading(self, loading: bool, message: str = ""):
        """Set loading state"""
        self.is_loading = loading
        
        if loading:
            self.signin_button.config(text=message, state='disabled')
            self.microsoft_button.config(state='disabled')
            self.email_entry.config(state='disabled')
            self.password_entry.config(state='disabled')
            self.status_label.config(text="", foreground='blue')
        else:
            self.signin_button.config(text="Sign in", state='normal')
            self.microsoft_button.config(state='normal')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
    
    def show_error(self, message: str):
        """Show error message"""
        self.status_label.config(text=message, foreground='red')
        
        # Clear error after 5 seconds
        self.parent.after(5000, lambda: self.status_label.config(text=""))
    
    def destroy(self):
        """Clean up the window"""
        # Unbind events
        self.parent.unbind('<Return>')
        
        # Clear widgets
        for widget in self.parent.winfo_children():
            widget.destroy()