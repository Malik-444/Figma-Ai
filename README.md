# AI Chat Desktop Application

A Python desktop application with AI chat capabilities, authentication, and system tray integration. This is a Python conversion of the original React/TypeScript web application.

## Features

- **Authentication**: Email/password and Microsoft SSO support
- **AI Chat Interface**: Interactive chat with AI assistant
- **System Tray Integration**: Minimize to tray on Windows and Mac
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Configurable**: Customizable settings and themes
- **Offline Capable**: Works with mock responses or real AI APIs

## Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)
- See `requirements.txt` for additional dependencies

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Authentication
- Use demo credentials: `demo@example.com` / `password123`
- Or click "Continue with Microsoft" for SSO (mock implementation)

### Chat Interface
- Type messages and press Enter to send
- AI responds with contextual replies
- Use Ctrl+M to minimize to system tray
- Use F11 for fullscreen mode

### System Tray
- Right-click tray icon for menu options
- Double-click to restore window
- Notifications show when minimized

## Configuration

Settings are stored in `~/.ai_chat_app/config.json`. You can modify:

- Window size and theme
- AI API settings
- Tray behavior
- Chat preferences

## Real AI Integration

To use real AI APIs instead of mock responses:

1. Install additional dependencies:
   ```bash
   pip install openai  # or anthropic
   ```

2. Set your API key in settings or config file:
   ```json
   {
     "ai": {
       "api_provider": "openai",
       "api_key": "your-api-key-here",
       "model": "gpt-3.5-turbo"
     }
   }
   ```

3. Update `app_controller.py` to use `call_real_ai_api()` instead of `generate_ai_response()`

## Microsoft SSO Integration

For real Microsoft authentication:

1. Install MSAL:
   ```bash
   pip install msal
   ```

2. Register your app in Azure AD
3. Update the authentication flow in `app_controller.py`

## Building Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
```

## Project Structure

```
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── app_controller.py  # Business logic and API calls
│   ├── tray_manager.py    # System tray integration
│   └── ui/
│       ├── __init__.py
│       ├── auth_window.py # Authentication interface
│       └── chat_window.py # Chat interface
└── assets/                # Icons and resources (optional)
    └── icon.ico
```

## Development

This application demonstrates:

- Modern Python GUI development with tkinter
- System tray integration across platforms
- API integration patterns
- Configuration management
- Authentication flows
- Real-time chat interfaces

## License

This project is provided as-is for educational and demonstration purposes.

## Migration from React/TypeScript

This Python application replicates the functionality of the original React/TypeScript web application:

- ✅ Authentication with email/password and Microsoft SSO
- ✅ AI chat interface with message history
- ✅ System tray integration (Windows/Mac)
- ✅ Responsive UI with modern styling
- ✅ Configuration management
- ✅ Real-time typing indicators
- ✅ Notification system

The Python version provides native desktop integration while maintaining the same user experience and feature set.