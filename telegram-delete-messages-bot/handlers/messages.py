from telegram import Update
from telegram.ext import CallbackContext, Filters

from .decorators import message
from settings import KEYWORDS_TO_DELETE


@message(Filters.text)
def delete_text(update: Update, context: CallbackContext):
    """Delets any messages that contain any of the keywords set within
    the KEYWORDS_TO_DELETE setting."""
    message = update.message.text
    if any(keyword in message for keyword in KEYWORDS_TO_DELETE):
        update.message.delete()