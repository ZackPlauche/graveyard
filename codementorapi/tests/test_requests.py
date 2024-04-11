import pandas as pd
from codementorapi import CodementorAPI
from codementorapi.models import Request

def test_get_requests(codementor: CodementorAPI):
    requests = codementor.get_open_requests()
    assert isinstance(requests, list)
    assert all([isinstance(request, Request) for request in requests])