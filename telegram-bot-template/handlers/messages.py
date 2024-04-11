from telegram import Update
from telegram.ext import CallbackContext, Filters

from .decorators import message


@message(Filters.text & (~Filters.command))
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


@message(Filters.command)
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")