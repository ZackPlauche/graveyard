import time

from pages import FormPage

from wyzantapi.models import Account


class LoginPage(FormPage):
    url = 'https://www.wyzant.com/login'
    post_submit_wait_time = 5
    success_url = 'https://www.wyzant.com/tutor/home'

    def login(self, account: Account) -> bool:
        username, password = account.login_info()
        self.driver.find_elements('id', 'Username')[-1].send_keys(username)
        self.driver.find_elements('id', 'Password')[-1].send_keys(password)
        self._get_submit_button().click()
        success = self._wait_for_success()
        return success

    def _get_submit_button(self):
        buttons = self.driver.find_elements('css selector', 'button[type="submit"]')
        submit_button = [button for button in buttons if button.text.casefold() == 'log in'][0]
        return submit_button

    def _wait_for_success(self) -> bool:
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            print(f'⌛ {round(elapsed_time, 2)} seconds elapsed', end='\r')
            if self.driver.current_url == self.success_url:
                print(f'⌛ {round(elapsed_time, 2)} seconds elapsed')
                print('✅ Login successful')
                return True
            if elapsed_time > self.post_submit_wait_time:
                print(f'⌛ {round(elapsed_time, 2)} seconds elapsed')
                print('❌ Login unsuccessful')
                return False
