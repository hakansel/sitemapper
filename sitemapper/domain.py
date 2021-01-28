ACCEPTED_CONTENT_TYPE = 'text/html'


class Page:

    def __init__(self, url, content) -> None:
        super().__init__()
        self.url = url
        self.content = content

    def __eq__(self, o: object) -> bool:
        return self.url == o.url

    def __hash__(self) -> int:
        return hash(self.url)
