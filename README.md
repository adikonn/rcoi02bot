# Rcoi02bot 🤖
Simple telegram bot for exam result checking 📊✅

## ✨ Features:

- 🔍 Exam Result Checking - Quick and easy result lookup
- 👤 User Registration - Simple registration process
- 📱 Telegram Integration - Native Telegram bot interface
- 🔔 Notifications - Automated result notifications
- 📊 Result Parsing - Intelligent result data processing
- 🛡️ Error Handling - Robust error management
- 📝 Logging - Comprehensive activity logging

## 🚀 Installation
Prerequisites
- Python 3.8+ 🐍
- pip package manager 📦
- Telegram Bot Token 🔑

## Setup Steps
1. Clone the repository 📥

```bash
git clone <your-repository-url>
cd rcoi02bot
```
2. Install dependencies ⚙️

```bash
pip install -r requirements.txt
```
3. Create environment file 🔧

```bash
cp .env.example .env
```
⚠️ Don't forget to create .env file!!! This is crucial for the bot to work properly.

4. Run the bot 🏃‍♂️
```bash
python main.py
```

## ⚙️ Configuration
Edit your .env file with the following variables:

```text
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
BOT_USERNAME=your_bot_username

# Database Configuration
DATABASE_URL=your_database_url

# API Configuration
RESULTS_API_URL=your_results_api_endpoint
API_KEY=your_api_key

# Logging
LOG_LEVEL=INFO
```
## 📁 Project Structure
```text
├── .env                    # Environment variables 🔐
├── requirements.txt        # Python dependencies 📋
├── main.py                # Application entry point 🚪
├── config/
│   └── settings.py        # App configuration ⚙️
├── core/
│   ├── bot.py            # Bot initialization 🤖
│   └── dispatcher.py     # Event dispatcher 📡
├── handlers/
│   ├── registration.py   # Registration handlers 👤
│   ├── results.py        # Result handlers 📊
│   └── common.py         # Common handlers 🔧
├── states/
│   └── registration.py   # FSM states 🔄
├── middleware/
│   ├── logging.py        # Logging middleware 📝
│   └── error_handler.py  # Error handling 🛡️
├── database/
│   ├── models.py         # Database models 🗄️
│   └── repository.py     # Data access layer 💾
├── services/
│   ├── result_service.py      # Result processing 📊
│   └── notification_service.py # Notifications 🔔
├── utils/
│   └── parsers.py        # Data parsers 🔍
└── tests/
    ├── test_handlers.py  # Handler tests ✅
    └── test_services.py  # Service tests ✅
```
## 🎯 Usage
Basic Commands
- /start - Initialize the bot 🚀
- /register - Register for result checking 📝
- /check - Check exam results 🔍
- /help - Show available commands ❓

### Registration Process
1. Send /register command 📝
2. Follow the step-by-step registration 👣
3. Provide required information 📋
4. Confirm registration ✅

### Checking Results
1. Use /check command 🔍
2. Bot will fetch your latest results 📊
3. Receive formatted result notification 📱

## 🛠️ Development
Running in Development Mode
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with debug logging
LOG_LEVEL=DEBUG python main.py
```

### 🤝 Contributing
1. Fork the repository 🍴
2. Create a feature branch 🌿
3. Make your changes ✏️
4. Add tests for new functionality ✅
5. Submit a pull request 📤

### 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

### 🆘 Support
1. If you encounter any issues:
2. Check the logs for error messages 📝
3. Verify your .env configuration ⚙️
4. Ensure all dependencies are installed 📦
5. Create an issue on GitHub 🐛

Made with ❤️ for easy exam result checking! 🎓✨
