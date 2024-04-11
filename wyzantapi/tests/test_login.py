from wyzantapi import WyzantAPI


def test_login(chrome_driver):
    wyzant = WyzantAPI.from_env(chrome_driver)
    assert wyzant.login()