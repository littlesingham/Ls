# JioTV Recording Bot for Telegram

A Telegram bot that records JioTV live streams and manages your recordings.

## Features

- 📺 Record JioTV channels directly from Telegram
- 💾 Manage recordings (list, delete, download)
- 🔔 Get notifications when recordings complete
- ⏰ Schedule recordings for future broadcasts
- 🎯 Search and select channels easily
- 📊 View recording status and storage

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from @BotFather)
- JioTV credentials (Mobile number + OTP)
- FFmpeg installed on your system

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/littlesingham/Ls.git
cd Ls
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the bot

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
JIOTV_USERNAME=your_jio_mobile_number
RECORDINGS_DIR=./recordings
```

### 4. Run the bot

```bash
python main.py
```

## Usage

### Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see available options |
| `/channels` | List all available JioTV channels |
| `/record` | Start recording a channel |
| `/recordings` | View your saved recordings |
| `/schedule` | Schedule a recording for later |
| `/help` | Get help and documentation |

### Example Workflow

1. `/start` - Begin interaction with the bot
2. `/channels` - Browse available channels
3. `/record` - Select a channel and duration
4. Bot starts recording and sends updates
5. `/recordings` - Download your recorded file

## Architecture

```
Ls/
├── main.py                 # Bot entry point
├── requirements.txt        # Python dependencies
├── .env                    # Configuration (create this)
├── config/
│   └── settings.py        # Bot settings
├── bot/
│   ├── __init__.py
│   ├── telegram_bot.py    # Telegram bot handlers
│   └── commands.py        # Command handlers
├── recorder/
│   ├── __init__.py
│   ├── jiotv_recorder.py  # JioTV recording logic
│   └── stream_handler.py  # Stream handling
├── channels/
│   ├── __init__.py
│   └── channel_manager.py # Channel management
├── database/
│   ├── __init__.py
│   └── db_manager.py      # SQLite database management
└── utils/
    ├── __init__.py
    └── helpers.py         # Utility functions
```

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `JIOTV_USERNAME` - JioTV mobile number
- `RECORDINGS_DIR` - Directory to store recordings
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Security & Legal

⚠️ **IMPORTANT**: This bot is for **educational purposes only**.

- This project is **not affiliated** with JioTV or Reliance Jio
- Use only for **personal, non-commercial purposes**
- Respect copyright and intellectual property rights
- The author is **not responsible** for misuse of this tool

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the GPL v3 License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 **Email**: jitendraunatti@pm.me
- 💬 **Telegram Channel**: https://t.me/jitendraunatti_github
- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/littlesingham/Ls/issues)

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for complying with applicable laws and terms of service. Recording copyrighted content without permission may violate intellectual property laws.

---

**⭐ Star this repository if you find it useful!**

© 2024 - Created by littlesingham
