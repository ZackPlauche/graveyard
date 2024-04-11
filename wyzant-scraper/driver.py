from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from brave import BRAVE_USER_DATA_PATH, BRAVE_EXE_PATH, BRAVE_PROFILE_DIR

# Selenium options to be logged into the primary Chrome account already
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = str(BRAVE_EXE_PATH)
chrome_options.add_argument(f'--user-data-dir={BRAVE_USER_DATA_PATH}')
chrome_options.add_argument(f'--profile-directory={BRAVE_PROFILE_DIR}')
chrome_options.add_argument('--start-maximized')


def start_driver():
    """Create a new instance of the driver"""
    service = Service(executable_path='chromedriver_108.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def safe_get(url: str, driver: webdriver.Chrome):
    if driver.current_url != url:
        driver.get(url)
