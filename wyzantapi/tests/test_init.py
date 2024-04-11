import os

from wyzantapi import WyzantAPI
from wyzantapi.models import Account


def test_create_wyzantapi(chrome_driver):
    wyzant = WyzantAPI(
        account=Account(
            username='username',
            password='password'
        ),
        driver=chrome_driver,
    )
    assert wyzant


def test_from_env(chrome_driver):
    assert os.getenv('WYZANT_USERNAME'), 'WYZANT_USERNAME not set in .env'
    assert os.getenv('WYZANT_PASSWORD'), 'WYZANT_PASSWORD not set in .env'

    wyzant = WyzantAPI.from_env(chrome_driver)
    assert wyzant


def test_start(chrome_driver):
    wyzant = WyzantAPI.start(chrome_driver)
    assert wyzant

