from telegram import Update
from telegram.ext import CallbackContext

from handlers.decorators import command
from messages import DEFAULT_START_MESSAGE


@command
def start(update: Update, context: CallbackContext):
    """Controls bot behavior when a user types /start"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=DEFAULT_START_MESSAGE)


@command
def get_chat_id(update: Update, context: CallbackContext):
    """Returns the chat id of the current chat. Super useful."""

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{update.effective_chat.id}')


@command
def caps(update: Update, context: CallbackContext):
    """Returns a capitalized version of the given text after the command."""

    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

@command
def supportme(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='I know right?')
