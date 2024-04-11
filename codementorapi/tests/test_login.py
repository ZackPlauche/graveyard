from codementorapi import CodementorAPI
from codementorapi.pages import Dashboard


def test_login(codementor: CodementorAPI):
    codementor.login()
    assert codementor.driver.current_url == Dashboard.url