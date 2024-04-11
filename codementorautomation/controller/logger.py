import sys
import logging
import codecs


# Create a logger instance
logger = logging.getLogger('codementorcontroller')
logger.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S')

# Create a FileHandler to write log messages to the file
file_handler = logging.FileHandler("codementor.log", 'a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Wrap sys.stdout into a StreamWriter object with utf-8 encoding
stream = codecs.getwriter('utf-8')(sys.stdout.buffer)

# Create a StreamHandler to print log messages to the terminal with encoding
stream_handler = logging.StreamHandler(stream)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.propagate = False