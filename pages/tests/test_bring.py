from pages import Page
from selenium import webdriver


def test_bring():
    class GoogleSearchPage(Page):
        url = "https://google.com"

    driver = webdriver.Chrome()
    GoogleSearchPage.bring(driver)
    assert driver.url == GoogleSearchPage.url

