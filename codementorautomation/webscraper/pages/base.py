from pydantic import BaseModel
from selenium_objects import Page, DetailPage
from selenium.webdriver.remote.webdriver import WebDriver

from webscraper.utils import handle_challenges


class BasePage(Page):

    @classmethod
    def bring(cls, driver: WebDriver, **params):
        page = super().bring(driver, **params)
        handle_challenges(driver)
        return page


class BaseDetailPage(DetailPage):
    
        @classmethod
        def bring(cls, driver: WebDriver, instance: BaseModel, **params):
            page = super().bring(driver, instance, **params)
            handle_challenges(driver)
            return page