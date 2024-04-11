import logging
import time
import os

from selenium_objects.pages import FormPage


from webscraper.types import LoginDetails
from .pages import Dashboard


class LoginPage(FormPage):
    url = "https://www.codementor.io/login"
    success_url = "https://www.codementor.io/m/dashboard"
    post_submit_wait_time = 6.5

    def login(self, login_details: LoginDetails):
        """Attempt login to codementor.io."""
        logged_in = self.submit_login_form(login_details)
        if not logged_in:
            logging.info('❌ Login failed. Solve reCaptcha challenge to continue...')
            start = time.time()
            while self.driver.current_url != Dashboard.url:
                time_elapsed = round(time.time() - start, 2)
                print(f'⌛ {time_elapsed} seconds elapsed', end='\r')
            print(f'⌛ {time_elapsed} seconds elapsed')
        logging.info('✅ Login successful!')

    def submit_login_form(self, login_details: LoginDetails):
        """Submit login form with given login details."""
        self.bring(self.driver)
        self.driver.implicitly_wait(5)
        self.insert_username(login_details.email)
        self.insert_password(login_details.password)
        time.sleep(2)  # Submit button needs to wait for a second before getting clicked (no clue why)
        self.click_submit()
        time.sleep(self.post_submit_wait_time)
        success = self.driver.current_url == self.success_url
        return success

    def insert_username(self, username: str):
        """Insert username into username input field."""
        username_input = self.driver.find_element('css selector', 'input[name="email"]')
        username_input.send_keys(username)

    def insert_password(self, password: str):
        """Insert password into password input field."""
        password_input = self.driver.find_element('css selector', 'input[name="password"]')
        password_input.send_keys(password)

    def click_submit(self):
        """Click submit button."""
        submit_button = self.driver.find_element('css selector', 'button[type="submit"]')
        submit_button.click()

    def detect_recaptcha_challenge(self):
        """Detect if reCaptcha challenge is present."""
        # TODO: This currently doesn't work.
        captcha_container = self.driver.find_element('id', 'captcha-container')
        return bool(captcha_container)