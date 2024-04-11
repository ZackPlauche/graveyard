import logging
import codecs
import sys


# Create a logger instance
logger = logging.getLogger('wyzantautomation')
logger.setLevel(logging.INFO)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')

# Create a FileHandler to write log messages to the file
file_handler = logging.FileHandler("wyzant.log", 'a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Wrap sys.stdout into a StreamWriter object with utf-8 encoding
stream = codecs.getwriter('utf-8')(sys.stdout.buffer)

# Create a StreamHandler to print log messages to the terminal with encoding
stream_handler = logging.StreamHandler(stream)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.propagate = False