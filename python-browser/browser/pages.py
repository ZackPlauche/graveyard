class Page:
    """A page to open in the browser."""

    def __init__(self, url: 'str | Page', load_time: int | float = 0):
        if isinstance(url, Page):
            page = url
            self.url = page.url
            self.load_time = page.load_time
            if load_time:
                self.load_time = load_time
        else:
            self.url = url
            self.load_time = load_time

    def __str__(self):
        return self.url

    def __add__(self, other: 'str | Page'):
        return Page(self.url + str(other), self.load_time)

    def with_url(self, url: str):
        """Replace the url."""
        return Page(url, self.load_time)
    
    def with_params(self, **params):
        """Add parameters to the url."""
        return Page(self.url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()]), self.load_time)