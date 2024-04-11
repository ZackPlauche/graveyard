import typing
import logging
from datetime import datetime
from functools import wraps
from pathlib import Path

from browsers.pages import Page
from proposal_sender.settings import SCREENSHOT_DIR

if typing.TYPE_CHECKING:
    from .base import Platform


def requires_page(page: Page, new_tab: bool = False):
    """Decorator to ensure the current page is the required page."""
    def decorator(func):
        @wraps(func)
        def wrapper(self: 'Platform', *args, **kwargs):
            while True:
                try:
                    self.browser.open_page(page, new_tab=new_tab)
                    if not self.browser.url == page.url:
                        raise Exception(f'Could not open page {page.url}')
                    break
                except Exception as e:
                    if self.login_page.url in self.browser.url:
                        self.login()
                    else:
                        raise e
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def screenshot_on_error(retry: bool = False):
    """Decorator to take a screenshot if an error occurs."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f'🚨 Error occurred on function {func.__name__}: {e}') 
                    args[0].browser.save_screenshot(SCREENSHOT_DIR / f'{func.__name__}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
                    if retry:
                        logging.info('🔄️ Retrying... 🔄️')
                        continue
                    else:
                        raise e
        return wrapper
    return decorator



def pad_message(message: str, min_chars: int) -> str:
    """Pad a message with spaces to reach a minimum number of characters"""
    return message + ' ' * (min_chars + 1 - len(message))


def build_screenshot_path() -> Path:
    """Build the path for the screenshot"""
    return SCREENSHOT_DIR / f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'