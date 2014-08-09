from __future__ import absolute_import

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from ..utils import resolve_url

urlparse.uses_netloc.append('paypalrest')

DEFAULT_ENV = 'PAYPAL'

def from_url(url=None, env=None):
    url = resolve_url(url, env, DEFAULT_ENV)

    if url is None:
        return None

    url = urlparse.urlparse(url)

    config = {
        'mode': url.hostname,
        'client_id': url.username,
        'client_secret': url.password,
    }
    return config

def to_url(config):
    config = config.copy()
    return "paypalrest://{client_id}:{client_secret}@{mode}".format(**config)
