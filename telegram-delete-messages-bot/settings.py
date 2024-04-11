TOKEN = ''

DEFAULT_START_MESSAGE = 'I\'m a bot, talk to me!'

KEYWORDS_TO_DELETE = [
    'https://t.me/',
    # ...
]


try:
    from local_settings import *
except ImportError:
    pass
