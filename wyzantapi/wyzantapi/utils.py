from datetime import datetime, timedelta
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_element_text(driver: WebDriver, element: str, expected_text: str, timeout: int = 10) -> bool:
    return WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element((By.XPATH, element), expected_text))


def pad_message(message: str, min_chars: int) -> str:
    """Pad a message with spaces to reach a minimum number of characters"""
    return message + ' ' * (min_chars + 1 - len(message))


def clean_text(text: str) -> str:
    text = clean_special_symbols(text)
    text = trim_newlines(text)
    return text.strip()


def clean_special_symbols(text: str) -> str:
    symbols = [
        ('’', "'")
    ]
    for symbol in symbols:
        text = text.replace(*symbol)
    return text


def trim_newlines(text):
    # Use regular expression to remove extra newlines before and after the content
    trimmed_text = re.sub(r'^\n+|\n+$', '', text)
    return trimmed_text
