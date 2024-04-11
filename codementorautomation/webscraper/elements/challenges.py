import time
from typing import ClassVar

from selenium_objects import Element, Selector

from selenium.webdriver.remote.webdriver import WebDriver



class BaseChallenge(Element):
    """Base class for challenges."""
    selector: ClassVar[Selector]

    @classmethod
    def handle(cls, driver: WebDriver):
        driver.implicitly_wait(2)
        if cls.exists(driver=driver):
            cls.find(driver=driver).solve()

    def solve(self):
        """Solve the challenge."""
        raise NotImplementedError('Challenge must implement a solve method.')

    def solve_manually(self):
        """Solve the human verification challenge manually."""
        driver_has_options = hasattr(self.driver, 'options')
        if driver_has_options:
            driver_options = self.driver.options.arguments
            if '--headless' in driver_options and '--user-data-dir' in driver_options:
                self._solve_with_headless_default_profile()
        else:
            self._watch_for_solve()

    def _watch_for_solve(self):
        start = time.time()
        while True:
            time_elapsed = round(time.time() - start, 2)
            if self.is_active:
                print(f'⏳ {time_elapsed} seconds elapsed', end='\r')
                continue
            print(f'⏳ {time_elapsed} seconds elapsed')
            print('✅ Human verification challenge resolved')
            break

    def _solve_with_headless_default_profile(self, driver: WebDriver):
        """Handles the human verification challenge when using a headless 
        driver with a default profile.

        NOTE: You must close the driver because you're using a default profile, 
        which can only have one instance of itself open at a time.
        """
        self.driver.quit()
        original_options = self.driver.options.copy()
        new_options = self.driver.options.copy()
        new_options.arguments.remove('--headless')
        new_temp_driver = self.driver.__class__(options=new_options)
        new_temp_driver.get('https://www.codementor.io/m/dashboard')
        
        # Wait and detect the human verification challenge to be resolved.
        # May want to run additional checks here to ensure everything is working smoothly.
        self.watch_for_solve()
        time.sleep(2)
        # Quit the new driver
        new_temp_driver.quit()
        # Reopen a new instance of the original driver
        self.driver = self.driver.__class__(options=original_options)

    @property
    def is_active(self) -> bool:
        """Detect if the human verification challenge is active."""
        return self.exists(self.driver)


class HumanVerificationChallenge(BaseChallenge):
    selector = Selector(by='id', value='captcha-container')

    def solve(self):
        """Solve the human verification challenge."""
        self.solve_manually()
