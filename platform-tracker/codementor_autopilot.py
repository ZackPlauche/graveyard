import logging
from proposal_sender.platforms import Codementor
from proposal_sender.settings import LOGS_DIR
from browsers import get_available_browser, chrome, chrome_beta, brave

detailed_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
simple_formatter = logging.Formatter('%(message)s - %(asctime)s')

logging.basicConfig(
    filename=LOGS_DIR / 'codementor_autopilot.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    encoding='utf-8'
)

# Add console logging with the simple formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(simple_formatter)
logging.getLogger().addHandler(console_handler)


# Log both to file and console WHILE STILL SUPPRESSING LOGS FROM THE SELENIUM LIBRARY AND URLLIB3
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

if __name__ == '__main__':
    browser = get_available_browser([chrome, chrome_beta, brave], headless=True)
    logging.info(str(browser))
    codementor = Codementor(browser, evaluate_manually=False)
    try:
        codementor.autopilot()
    except Exception as e:
        logging.exception(e)
        raise e