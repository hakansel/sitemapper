import os

from sitemapper.app import CrawlerApp

DEFAULT_DEST_URL = 'https://www.afiniti.com/'

if __name__ == '__main__':
    url = os.getenv('DEST_URL')
    if url:
        CrawlerApp().run(url=url)
    else:
        CrawlerApp().run(url=DEFAULT_DEST_URL)
