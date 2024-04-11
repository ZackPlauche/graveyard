from pathlib import Path
from browser import Browser

BASE_DIR = Path(__file__).parent.parent
DRIVERS_DIR = BASE_DIR / 'drivers'

chromedriver_108 = DRIVERS_DIR / 'chromedriver_108.exe'
chromedriver_110 = DRIVERS_DIR / 'chromedriver_110.exe'
chromedriver_111 = DRIVERS_DIR / 'chromedriver_111.exe'
chromedriver_112 = DRIVERS_DIR / 'chromedriver_112.exe'
chromedriver_113 = DRIVERS_DIR / 'chromedriver_113.exe'

chrome = Browser(
    name='Chrome',
    driver_path=chromedriver_113,
    user_data_path=Path.home() / 'AppData/Local/Google/Chrome/User Data',
    exe_path='C:/Program Files/Google/Chrome/Application/chrome.exe',
)

chrome_beta = Browser(
    name='Chrome Beta',
    driver_path=chromedriver_112,
    user_data_path=Path.home() / 'AppData/Local/Google/Chrome Beta/User Data',
    exe_path='C:/Program Files/Google/Chrome Beta/Application/chrome.exe'
)

brave = Browser(
    name='Brave',
    driver_path=chromedriver_112,
    user_data_path=Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data',
    exe_path='C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
)