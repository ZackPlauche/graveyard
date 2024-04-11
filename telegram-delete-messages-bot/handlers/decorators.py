from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler


def command(func):
    """
    Shortcut decorator function for assigning a CommandHandler to a function. 
    Uses the function name as the command name.
    """
    return CommandHandler(func.__name__, func)


def inline(func):
    """
    Shortcut decorator function for assigning an InlineQueryHandler to a function.
    """

    return InlineQueryHandler(func)


def message(filters):
    """
    Shortcut decorator function for assigning MessageHandlers.
    Takes in a required argument filters (the same filters used for MessageHandler).
    """

    def decorator(func):
        return MessageHandler(filters, func)
    return decorator
