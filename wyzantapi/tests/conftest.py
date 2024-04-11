from pathlib import Path

import pytest
from selenium import webdriver

IGNORE_DIR = Path(__file__).parent.parent / 'ignore'
if not IGNORE_DIR.exists():
    IGNORE_DIR.mkdir()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption('-H', '--headless', action='store_true', default=False, help='Run tests in headless mode.')
    parser.addoption('-D', '--default-profile', action='store_true', default=False, help='Run tests with default profile.')


@pytest.fixture(scope='session')
def chrome_driver(request: pytest.FixtureRequest) -> webdriver.Chrome:
    headless_mode = request.config.getoption('--headless')
    default_profile = request.config.getoption('--default-profile')

    # Set global_options
    global_options = webdriver.ChromeOptions()
    if headless_mode:
        global_options.add_argument('--headless=new')
    if default_profile:
        user_data_dir = Path.home() / 'AppData/Local/Google/Chrome/User Data'
        default_profile = 'Default'
        global_options.add_argument(f'--user-data-dir={user_data_dir}')
        global_options.add_argument(f'--profile-directory={default_profile}')

    driver = webdriver.Chrome(options=global_options)

    def teardown():
        driver.quit()

    request.addfinalizer(teardown)
    return driver


@pytest.fixture(scope='session')
def data_dir() -> Path:
    return IGNORE_DIR
