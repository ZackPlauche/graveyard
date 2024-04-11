import logging

from telegram.ext import Updater, Dispatcher

from config import TOKEN
from handlers.commands import start, caps, supportme, get_chat_id
from handlers.messages import unknown
from handlers.inlines import inline_caps



def main() -> None:
    updater = Updater(TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    # Add your handlers here.
    dispatcher.add_handler(start)
    dispatcher.add_handler(caps)
    dispatcher.add_handler(get_chat_id)
    dispatcher.add_handler(supportme)
    dispatcher.add_handler(inline_caps)
    dispatcher.add_handler(unknown)

    # Start bot
    updater.start_polling()
    updater.idle()  # Allow Ctrl + c to stop the bot.

if __name__ == '__main__':
    # Bot logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()