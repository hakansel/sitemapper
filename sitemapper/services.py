import json
import threading
from typing import Optional

from sitemapper.domain import Page
from sitemapper.utils import HtmlUtils


class CrawlerService(object):
    url_queue: set
    fetching_queue: set
    content_queue: set
    parallelism: int

    url_map: dict

    def __init__(self, root_url: str) -> None:
        super().__init__()
        self.root_url = root_url
        self._lock = threading.Lock()

        self.url_queue = set()
        self.fetching_queue = set()
        self.content_queue = set()
        self.parallelism = 25

        self.url_map = ({})

    def start(self):
        self.url_queue.add(self.root_url)
        t = threading.Thread(target=self._parse_content, daemon=False)
        t.start()
        for i in range(0, self.parallelism):
            threading.Thread(target=self._fetch_page, daemon=True).start()
        t.join()

    def print_result(self):
        print("== Accessible Web Pages ==")
        for _url in self.url_map.keys():
            print("\t" + _url)
        depth = 0
        waiting_url = dict()
        waiting_url[self.root_url] = 0
        traced_url = set()
        sitemap = self._trace(self.root_url, depth, waiting_url, traced_url)
        print("\n\n== Web Pages Sitemap ==")
        print(json.dumps(sitemap, indent=2))

    def _trace(self, url, depth, waiting_url, traced_url):
        children = []
        for _url in self.url_map.get(url, url):
            if _url not in waiting_url.keys():
                waiting_url[_url] = waiting_url[url] + 1
        for _url in self.url_map.get(url, url):
            if depth < waiting_url[_url] and _url not in traced_url:
                children.append(self._trace(_url, depth + 1, waiting_url, traced_url))
                traced_url.add(_url)
        return {"url": url, "children": children}

    def _parse_content(self):
        while len(self.url_queue) > 0 or len(self.fetching_queue) > 0 or len(self.content_queue) > 0:
            if len(self.content_queue) > 0:
                page = self.content_queue.pop()
                child_urls = set()
                if page.content:
                    child_urls = HtmlUtils.parse_urls(page.url, page.content)
                    for child in child_urls:
                        if child.startswith(self.root_url):
                            self.url_queue.add(child)
                        else:
                            self.url_map[child] = []
                self.url_map[page.url] = list(child_urls)

    def _fetch_page(self):
        while len(self.url_queue) > 0 or len(self.fetching_queue) > 0 or len(self.content_queue) > 0:
            new_url = self._pop_url()
            if new_url and new_url not in self.url_map.keys():
                url, content = self._get_page_content(url=new_url)
                self.content_queue.add(Page(url=url, content=content))

    def _pop_url(self) -> Optional[str]:
        with self._lock:
            if len(self.url_queue) > 0:
                new_url = self.url_queue.pop()
                return new_url
            else:
                return None

    def _get_page_content(self, url: str):
        content = None
        if url not in self.fetching_queue:
            self.fetching_queue.add(url)
            content = HtmlUtils.get_content(url)
            self.fetching_queue.remove(url)
        return url, content
