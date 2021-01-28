import re
import urllib.parse
import urllib.request

from sitemapper.domain import ACCEPTED_CONTENT_TYPE


class HtmlUtils(object):

    @staticmethod
    def get_content(url):
        content = None
        try:
            response = urllib.request.urlopen(url)
            if 200 == response.status and ACCEPTED_CONTENT_TYPE in response.headers.get('content-type'):
                content = response.read().decode(encoding='utf-8', errors='replace')
        except Exception as e:
            pass
        return content

    @staticmethod
    def parse_urls(url: str, content: str) -> set:
        child_urls = set()
        urls = re.findall(r'(?i)href=["\']?([^\s"\'<>]+)', content)
        for _url in urls:
            if not _url.startswith('mailto:') and not _url.startswith('tel:'):
                full_url = urllib.parse.urljoin(url, _url)
                if full_url.endswith("/"):
                    full_url = full_url[:1]
                if '#' in full_url:
                    full_url = full_url.split("#", maxsplit=1)[0]
                child_urls.add(full_url)
        return child_urls
