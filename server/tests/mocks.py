class MockResponse:
    """
    Mock of Response object from the requests package
    https://requests.readthedocs.io/en/latest/api/#requests.Response
    """

    def __init__(self, status_code: int, data) -> None:
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data
