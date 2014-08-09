from __future__ import absolute_import

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from ..utils import resolve_url, QueryDict

urlparse.uses_netloc.append('redis')

DEFAULT_ENV = 'REDIS_URL'

def from_url(url=None, env=None):
    url = resolve_url(url, env, DEFAULT_ENV)

    if url is None:
        return None

    url = urlparse.urlparse(url)
    path = url.path[1:] # remove forward slash, if any.

    params = QueryDict(url.query)
    # Update with environment configuration.
    config = {
        'db': int(path or 0),
        'host': url.hostname,
        'port': url.port or 6379,
    }
    if url.username:
        config['password'] = url.username
    if params:
        config.update(params)
    return config

def to_url(config):
    config = config.copy()
    if config['password']:
        base_url = "redis://{password}@{host}:{port}/{db}".format(**config)
    else:
        base_url = "redis://{host}:{port}/{db}".format(**config)

    remaining_options = {k:v[0] for k,v in config.items() if not k in ['password', 'host', 'port', 'db']}
    query = QueryDict('', mutable=True)
    query.update(remaining_options)
    if query:
        return base_url + "?" + query.urlencode()
    else:
        return base_url