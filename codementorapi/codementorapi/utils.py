import os
from datetime import timedelta
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


from codementorapi.elements.challenges import HumanVerificationChallenge

def build_options(sneaky=True, default_profile=False, headless=False):
    """General chrome options builder for selenium webdriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    if sneaky:
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
    if default_profile:
        user_data_dir = Path.home() / 'AppData/Local/Google/Chrome/User Data'
        default_profile = 'Default'
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_argument(f'--profile-directory={default_profile}')
    if headless:
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
    return options


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


def pause():
    os.system('pause')  


def handle_challenges(driver: WebDriver):
    driver.implicitly_wait(5)
    HumanVerificationChallenge.handle(driver=driver)
