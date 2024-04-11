import logging
import subprocess
import time
from dataclasses import dataclass
from functools import wraps
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement

from .pages import Page


def requires_start(func):
    """Decorator to ensure the browser is started."""
    @wraps(func)
    def wrapper(self: 'Browser', *args, **kwargs):
        if not self.driver:
            self.start()
        return func(self, *args, **kwargs)
    return wrapper


@dataclass
class Browser:
    name: str
    driver_path: str | Path
    user_data_path: str | Path
    exe_path: str | Path | None = None
    profile_dir: str = 'Default'
    headless: bool = False
    driver: webdriver.Chrome | None = None

    def __post_init__(self):
        self.options = Options()
        self.options.add_argument(f'--user-data-dir={self.user_data_path}')
        self.options.add_argument(f'--profile-directory={self.profile_dir}')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--start-maximized')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if self.exe_path:
            self.options.binary_location = str(self.exe_path)

        self.service = Service(executable_path=str(self.driver_path))

    def __str__(self):
        return f'Browser: {self.name} - Session ID: {self.session_id}'

    def start(self):
        """Start the browser."""
        if self.headless:
            self.options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def close(self):
        """Close the current tab."""
        self.driver.close()

    def quit(self):
        """Quit the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    @requires_start
    def open_page(self, page: str | Page, load_time: float = 0, new_tab: bool = False):
        """Open a page and wait for it to load."""

        # Build page
        page = Page(page)
        if load_time:
            page.load_time = load_time

        # 1. If page is already open: do nothing
        if self.driver.current_url == page.url:
            return
        # 2. If new_tab is set, open the page in a new tab
        elif new_tab:
            self.open_new_tab(page.url)
        # 3. Otherwise, open the page in the current tab
        else:
            self.driver.get(page.url)

        # Wait for page to load
        if page.load_time:
            time.sleep(page.load_time)

    def get(self, url: str | Page, load_time: float = 0, new_tab: bool = False):
        """Shortcut for open_page."""
        self.open_page(url, load_time, new_tab)

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def implicitly_wait(self, seconds: int):
        """Set the implicit wait time."""
        self.driver.implicitly_wait(seconds)

    @property
    def window_handles(self):
        """Return the window handles."""
        return self.driver.window_handles

    @property
    def session_id(self):
        """Return the session id."""
        return self.driver.session_id

    @property
    def url(self):
        """Shortcut for current_url."""
        return self.current_url

    @property
    def current_url(self):
        """Return the current url."""
        return self.driver.current_url
    
    @property
    def page_source(self):
        """Return the page source."""
        return self.driver.page_source

    @property
    def html(self):
        """Shortcut for page_source."""
        return self.page_source


    def find_element(self, by: str, selector: str):
        """Find an element by selector."""
        return self.driver.find_element(by, selector)

    def find_elements(self, by: str, selector: str):
        """Find elements by selector."""
        return self.driver.find_elements(by, selector)

    def remove_element(self, element: WebElement):
        """Remove an element from the DOM."""
        self.driver.execute_script("arguments[0].remove()", element)

    def send_keys_with_emojis(self, element: WebElement, message: str):
        """send_keys function that can also sends emojis."""
        self.driver.execute_script("arguments[0].value += arguments[1]", element, message)

    def open_new_tab(self, url: str):
        """Open url in a new tab and switch to it."""
        self.driver.execute_script(f"window.open('{url}');")
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def close_tab(self):
        """Close current tab and switch to the previous tab."""
        if len(self.driver.window_handles) == 1:
            logging.warn('⚠️ Tab attempted to be closed when only one tab is open. ⚠️')
            raise Exception('Tab attempted to be closed when only one tab is open.')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def count_tabs(self):
        """Return number of open tabs."""
        return len(self.driver.window_handles)
    
    def save_screenshot(self, filename: str | Path | None = None):
        """Save a screenshot of the page."""
        return self.driver.save_screenshot(filename)

    def refresh(self):
        """Refresh the page."""
        self.driver.refresh()

    def copy(self):
        """Return a copy of the browser."""
        return Browser(
            name=self.name,
            driver_path=self.driver_path,
            user_data_path=self.user_data_path,
            exe_path=self.exe_path,
            profile_dir=self.profile_dir,
            headless=self.headless
        )

    def kill(self):
        """Kill running browser processes."""
        if self.exe_path:
            subprocess.run(['taskkill', '/F', '/IM', Path(self.exe_path).name], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
