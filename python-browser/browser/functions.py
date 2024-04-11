import requests
import logging
from typing import Iterable
from .browser import Browser
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def get_available_browser(browsers: Iterable[Browser], headless=False) -> Browser:  # type: ignore
    for browser in browsers:
        logging.debug(f'Trying browser: {browser.name}')
        try:
            if headless:
                browser.headless = True
            browser.start()
            return browser
        except Exception as e:
            feedback = browser.name + ' is currently in use.'
            feedfoward = 'Trying next browser.'
            logging.debug(feedback + ' ' + feedfoward)
            browser.quit()
            continue



def get_latest_chromedriver():
    url = 'https://chromedriver.chromium.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    current_releases_list = soup.select_one('#h\.e02b498c978340a_87 > div > div > ul:nth-child(3)')
    for release in current_releases_list.find_all('li'):
        release_a_tag = release.find('a')
        release_url = release_a_tag['href']
        release_version = parse_qs(urlparse(release_url).query).get('path')
        print(release_version, ': ', release_url)


    
