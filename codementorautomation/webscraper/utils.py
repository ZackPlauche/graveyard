from datetime import timedelta
from selenium.webdriver.remote.webdriver import WebDriver

from webscraper.elements.challenges import HumanVerificationChallenge


def parse_time_str(time_text: str) -> timedelta:
    """Returns a full timedelta from a time string like '1h 30m 30s'."""
    time_delta = timedelta()
    for time_text in time_text.split(' '):
        if time_text[-1] == 'h':
            time_delta += timedelta(hours=int(time_text[:-1]))
        elif time_text[-1] == 'm':
            time_delta += timedelta(minutes=int(time_text[:-1]))
        elif time_text[-1] == 's':
            time_delta += timedelta(seconds=int(time_text[:-1]))
    return time_delta


def handle_challenges(driver: WebDriver):
    """Handles all challenges."""
    driver.implicitly_wait(5)
    HumanVerificationChallenge.handle(driver=driver)
