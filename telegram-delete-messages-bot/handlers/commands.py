from telegram import Update
from telegram.ext import CallbackContext

from handlers.decorators import command
from settings import DEFAULT_START_MESSAGE


@command
def start(update: Update, context: CallbackContext):
    """Controls bot behavior when a user types /start"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=DEFAULT_START_MESSAGE)