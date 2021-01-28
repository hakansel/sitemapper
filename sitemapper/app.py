from sitemapper.services import CrawlerService


class CrawlerApp(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def run(self, url: str):
        service = CrawlerService(root_url=url)
        service.start()
        service.print_result()
