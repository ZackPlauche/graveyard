import logging

from telegram.ext import Updater, Dispatcher

from settings import TOKEN
from handlers.commands import start
from handlers.messages import delete_text


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    # Add your handlers here.
    dispatcher.add_handler(start)
    dispatcher.add_handler(delete_text)

    # Start bot
    updater.start_polling()
    updater.idle()  # Allow Ctrl + c to stop the bot.

if __name__ == '__main__':
    # Bot logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    main()