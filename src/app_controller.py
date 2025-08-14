"""
Application Controller
Handles business logic, authentication, and API interactions.
"""

import requests
import time
import json
import threading
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    id: str
    content: str
    sender: str  # 'user' or 'ai'
    timestamp: datetime

class AppController:
    def __init__(self):
        self.api_base_url = "https://api.openai.com/v1"  # Example AI API
        self.api_key = None
        self.messages = []
        self.is_typing = False
        self.message_callbacks = []
        
    def add_message_callback(self, callback: Callable):
        """Add callback for new messages"""
        self.message_callbacks.append(callback)
        
    def notify_message_callbacks(self, message: Message):
        """Notify all message callbacks"""
        for callback in self.message_callbacks:
            try:
                callback(message)
            except Exception as e:
                print(f"Error in message callback: {e}")
    
    def authenticate_email(self, email: str, password: str) -> bool:
        """Authenticate user with email and password"""
        # Mock authentication - in real app this would call your auth service
        if email == "demo@example.com" and password == "password123":
            return True
        return False
    
    def authenticate_microsoft(self) -> Optional[str]:
        """Authenticate with Microsoft SSO"""
        # Mock Microsoft authentication
        # In real app, this would use MSAL or similar library
        import webbrowser
        import time
        
        try:
            # Simulate OAuth flow
            auth_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
            params = {
                "client_id": "your-client-id",
                "response_type": "code",
                "redirect_uri": "http://localhost:8080/callback",
                "scope": "openid email profile",
                "response_mode": "query"
            }
            
            # In a real app, you'd open browser and handle OAuth flow
            # For demo, we'll just simulate success
            print("Opening Microsoft authentication (simulated)...")
            time.sleep(2)  # Simulate auth time
            
            return "user@microsoft.com"  # Mock successful auth
            
        except Exception as e:
            print(f"Microsoft auth error: {e}")
            return None
    
    def send_message_to_ai(self, message: str, callback: Callable[[str], None]):
        """Send message to AI API and handle response"""
        def ai_request():
            try:
                self.is_typing = True
                
                # Add user message
                user_msg = Message(
                    id=str(int(time.time() * 1000)),
                    content=message,
                    sender='user',
                    timestamp=datetime.now()
                )
                self.messages.append(user_msg)
                self.notify_message_callbacks(user_msg)
                
                # Simulate AI processing time
                time.sleep(1 + len(message) * 0.01)  # Realistic typing delay
                
                # Generate AI response (mock)
                ai_response = self.generate_ai_response(message)
                
                # Add AI message
                ai_msg = Message(
                    id=str(int(time.time() * 1000) + 1),
                    content=ai_response,
                    sender='ai',
                    timestamp=datetime.now()
                )
                self.messages.append(ai_msg)
                self.notify_message_callbacks(ai_msg)
                
                self.is_typing = False
                callback(ai_response)
                
            except Exception as e:
                self.is_typing = False
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                
                ai_msg = Message(
                    id=str(int(time.time() * 1000) + 1),
                    content=error_msg,
                    sender='ai',
                    timestamp=datetime.now()
                )
                self.messages.append(ai_msg)
                self.notify_message_callbacks(ai_msg)
                
                callback(error_msg)
        
        # Run in separate thread to avoid blocking UI
        threading.Thread(target=ai_request, daemon=True).start()
    
    def generate_ai_response(self, user_message: str) -> str:
        """Generate AI response (mock implementation)"""
        user_message_lower = user_message.lower()
        
        # Context-aware responses
        if any(word in user_message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your AI assistant. How can I help you today?"
        
        elif 'help' in user_message_lower:
            return ("I'm here to help! I can assist with various topics like answering questions, "
                   "brainstorming ideas, explaining concepts, or just having a conversation. "
                   "What would you like to discuss?")
        
        elif 'weather' in user_message_lower:
            return ("I don't have access to real-time weather data, but I'd recommend checking "
                   "a weather app or website for current conditions. Is there anything else I can help with?")
        
        elif 'python' in user_message_lower:
            return ("Python is a great programming language! It's known for its simplicity and readability. "
                   "Are you working on a specific Python project or have questions about Python development?")
        
        elif 'thank' in user_message_lower:
            return "You're welcome! Is there anything else I can help you with?"
        
        else:
            # Generic responses
            responses = [
                "That's an interesting question! Let me help you with that.",
                "I understand what you're asking. Here's my perspective on it:",
                "Great point! I can provide some insights about this topic.",
                "I'd be happy to help you explore this further.",
                "That's a thoughtful query. Let me break this down for you:",
                "I can definitely assist with that. Here's what I think:",
            ]
            
            import random
            base_response = random.choice(responses)
            
            return f"{base_response}\n\nYou mentioned: \"{user_message}\"\n\nThis is a mock response from the Python desktop application. In a production environment, this would be powered by a real AI API like OpenAI's GPT, Anthropic's Claude, or similar services."
    
    def call_real_ai_api(self, message: str) -> str:
        """Call real AI API (example implementation)"""
        if not self.api_key:
            raise Exception("API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    def get_message_history(self) -> list[Message]:
        """Get chat message history"""
        return self.messages.copy()
    
    def clear_message_history(self):
        """Clear chat message history"""
        self.messages.clear()
    
    def set_api_key(self, api_key: str):
        """Set AI API key"""
        self.api_key = api_key