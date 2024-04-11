from pathlib import Path

from selenium import webdriver


def build_options(sneaky=True, default_profile=False, headless=False) -> webdriver.ChromeOptions():
    """General chrome options builder for selenium webdriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    options.add_argument('--mute-audio')
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
