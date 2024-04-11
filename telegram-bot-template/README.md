# Telegram Bot Tempalte
![Random gif I found of a bot assembly plant](https://texterra.ru/upload/img/22-10-2019/bot.gif)

An easy to use quick start template for building telegram bots in Python.

## Requirements
- You'll need to have created a bot from the Bot Father in telegram to get the bot's auth token.


## Quickstart

1. Clone the repo: `git clone https://www.github.com/zackplauche/telegram-bot-template`
2. pip install the requirements into your project: `pip install -r requirements.txt`
3. Add your Telegram bot auth token to the `config/settings.py` or to a `config/locals.py` if you'd like.
4. Run the bot with the default commands: `bot.py`

Then customize. For more in depth setup, see below.

## How to use

**Step 1:** Clone the repo into your own directory

Using Git:
```cmd
git clone https://www.github.com/ZackPlauche/telegram-bot-template
```
Using GitHub CLI:
```cmd
gh repo clone ZackPlauche/telegram-bot-template
```

**Step 2:** Delete the `.git` folder and reset the contents of the  `README.md` file that come with the template to treat it as your own project and upload the bot to your own repo.

**Step 3:** Pip install the requirements to your python environment: `pip install -r requirements.txt`

**Step 4:** Fill in the `TOKEN` setting inside the `conf/settings.py` file with your your bot's auth token.
```py
TOKEN = ''  # <- Fill this one in

GROUP_CHAT_IDS = []  
```
 This is a global setting that you can use in any of your other files like so:
```py
from config import TOKEN
```
You can also add any global constant variables you'd like to be accessible anywhere in your app to this file, and your can import them the same way.

**Step 5:** Customize the handlers (the actions for your bot to execute) in the `handlers` directory. The different actions can be organized into the appropriate folders (see [handlers](#2-handlers) below for more details). Also be sure to try out the `handlers/decorators.py` file to see syntactic sugar versions of the `telegram-bot` packages different handlers.

**Step 6:** Register your handlers in the bot.py file.
```python
# bot.py
import logging

from telegram.ext import Updater, Dispatcher

from config import TOKEN
from handlers.commands import start, get_chat_id  # Example handlers


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    # Add your handlers here.
    dispatcher.add_handler(start)
    dispatcher.add_handler(get_chat_id)

    # Start bot
    updater.start_polling()
    updater.idle()  # Allow Ctrl + c to stop the bot.
```

**Step 7:** Start your bot.
```md
python bot.py
```

## How it's organized:

There are 3 main parts to this template:
### 1. Config
This is where you'll store your global settings (for example, the TOKEN for your bot) are stored in the default settings.py or a locals.py file in the same directory.

### 2. Handlers
Stored in `./handlers/`
This is where you'll store the actions and commands for your bot to follow. There is a separate folder for each type of handler, for example:
- **Command Handlers**: Stored in `handlers/commands.py`Handlers that run whenever your run a slash command (ex: `/help`)
- **Message handlers**: Handlers that react for certain types of messages (like `echo` that says repeats whatever a user says.)
- **Inline Queries**: Handlers for inilne commands where you @ your bot's name and choose an action from there.

### 3. bot.py 
This is the file where your bot actually runs from. This is where you'll register your handlers.

## God Mode
While your bot is running, or not, you can send commands directly from your command line / terminal **OR** your python interpretor to do things like send messages from your bot.


Send a message to every chat in the `GROUP_CHAT_IDS`
```cmd
python god.py send "Your message here"
```

Send a message to a single chat by providing the `chat_id` or an index of a chat in the `GROUP_CHAT_IDS`.

With `chat_id`:
```cmd
 python god.py send "Your message here" -123456789
```

With `GROUP_CHAT_ID` index:
```cmd
 python god.py send "Your message here" 0
```