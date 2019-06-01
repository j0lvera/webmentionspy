from webmentions.endpoint_discovery import make_url_absolute


def test_make_url_absolute():
    url = 'https://webmentions.rock'

    assert make_url_absolute('/path', url) == 'https://webmentions.rock/path'
    assert make_url_absolute(url, url) == url
