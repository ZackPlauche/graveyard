# Boof's Telegram Delete Bot
Initially created using [Telegram Bot Template](https://www.github.com/zackplauche/telegram-bot-template) by [Zack Plauché](https://www.zackplauche.com).

## Requirements
- A Telegram Bot from the Botfather with admin permissions in the group you'd like him to delete messages in.

## Setup
Install Python Requirements
```
pip install -r requirements.txt
```

## Getting Started

1. Add your bot token to the `TOKEN` setting in `settings.py`.
2. Add any additional keywords you'd like to delete to the `KEYWORDS_TO_DELETE` setting in `settings.py`.
3. Run the bot: `python bot.py`