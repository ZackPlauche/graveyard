from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext

from handlers.decorators import inline


@inline
def inline_caps(update: Update, context: CallbackContext):
    query: str = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)