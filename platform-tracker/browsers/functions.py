import logging
from typing import Iterable
from .browser import Browser


def get_available_browser(browsers: Iterable[Browser], headless=False) -> Browser:  # type: ignore
    for browser in browsers:
        logging.debug(f'Trying browser: {browser.name}')
        try:
            if headless:
                browser.headless = True
            browser.start()
            return browser
        except Exception as e:
            feedback = browser.name + ' is currently in use.'
            feedfoward = 'Trying next browser.'
            logging.debug(feedback + ' ' + feedfoward)
            browser.quit()
            continue
