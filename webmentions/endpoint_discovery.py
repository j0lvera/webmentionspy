from urllib.parse import urlparse
from lxml import html
import requests
import htmlmin

# https://www.w3.org/TR/webmention/#sender-discovers-receiver-webmention-endpoint-p-3

HEADERS = {'content-encoding': 'gzip', 'User-Agent': 'Webmention discovery'}
URL = 'https://webmention.rocks/test/11'


def make_url_absolute(path: str, url: str):
    if 'http' in path:
        return path

    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.hostname}{path}"


def discovery(url):
    page = requests.get(url, HEADERS)
    print('headers:', page.headers)

    if 'Link' in page.headers:
        link = page.headers['Link'].split(';')[0][1:-1]
        return make_url_absolute(link, url)

    if 'text/html' in page.headers['content-type']:
        minified_html = htmlmin.minify(page.text, remove_empty_space=True)
        tree = html.fromstring(minified_html)

        # Get first instance of link or a tag with rel value of `webmention`
        rels = tree.cssselect('[rel]')
        webmention_els = [el for el in rels if 'webmention' in el.get('rel')]
        href = webmention_els[0].get('href')
        return make_url_absolute(href, url)

    return False


print('result:', discovery(URL))

