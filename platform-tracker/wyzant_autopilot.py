import logging

from browsers import brave, chrome, chrome_beta, get_available_browser
from proposal_sender.platforms import Wyzant
from proposal_sender.settings import LOGS_DIR

# Log both to file and console WHILE STILL SUPPRESSING LOGS FROM THE SELENIUM LIBRARY AND URLLIB3
detailed_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
simple_formatter = logging.Formatter('%(message)s - %(asctime)s')

logging.basicConfig(
    filename=LOGS_DIR / 'wyzant_autopilot.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    encoding='utf-8'
)

# Add console logging with the simple formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(simple_formatter)
logging.getLogger().addHandler(console_handler)

logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

if __name__ == '__main__':
    browser = get_available_browser([chrome, chrome_beta, brave], headless=True)
    logging.info(str(browser))
    wyzant = Wyzant(browser)
    try:
        wyzant.autopilot()
    except Exception as e:
        logging.exception(e)
        raise e