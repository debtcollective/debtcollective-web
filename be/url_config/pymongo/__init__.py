from __future__ import absolute_import

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from ..utils import resolve_url

urlparse.uses_netloc.append('mongodb')

DEFAULT_ENV = 'MONGOHQ_URL'

def from_url(url=None, env=None):
    url = resolve_url(url, env, DEFAULT_ENV)

    if url is None:
        return None

    url = urlparse.urlparse(url)
    path = url.path[1:] # remove forward slash, if any.

    # Update with environment configuration.
    config = {
        'NAME': path,
        'HOST': url.hostname,
        'PORT': url.port,
    }
    for key, value in [('USER', url.username), ('PASSWORD', url.password)]:
        if value:
            config[key] = value
    return config

def to_url(config):
    config = config.copy()
    return "mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**config)
