from __future__ import absolute_import

from collections import defaultdict
from copy import deepcopy

from url_config.utils import six

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from url_config.utils import QueryDict, resolve_url, urlencode, bool_str

DEFAULT_ENV = 'MEMCACHE_URL'

SCHEMES = {
    'pylibmc': 'django_pylibmc.memcached.PyLibMCCache',
    'locmem': 'django.core.cache.backends.locmem.LocMemCache',
}

BACKENDS = {engine:scheme for scheme, engine in SCHEMES.items()}

for scheme in SCHEMES:
    # Register database schemes in URLs.
    urlparse.uses_netloc.append(scheme)

def from_url(url=None, env=None):
    url = resolve_url(url, env, DEFAULT_ENV)

    if url is None:
        return None

    # We have to do special work here because the "hostname" may really be multiple hosts
    # delimited by ";".  But if any of them have ports, this breaks urlparse
    # (as it is not a legal URL format).

    hostnames = url.split("//", 1 # remove scheme
        )[1].split("@" #remove auth
        )[-1].split('/', 1 # remove path
        )[0].split(";") #separate hostnames.

    if len(hostnames) == 1:
        hostnames = hostnames[0] # coerce back to string rather than list for single-node backends.

    url = urlparse.urlparse(url)

    if url.scheme in SCHEMES:
        config = {
            'BACKEND': SCHEMES[url.scheme],
        }
    else:
        raise ValueError("cache scheme {0} is not yet supported".format(url.scheme))

    config['LOCATION'] = hostnames

    if url.username:
        config['USERNAME'] = url.username
    if url.password:
        config['PASSWORD'] = url.password

    params = QueryDict(url.query)

    key_coercions = defaultdict(
        lambda: lambda value: value, # identity for most things
        {
            'TIMEOUT': int,
            'BINARY': lambda value: bool_str(value),
            'OPTIONS': lambda value: {k: key_coercions[k](v) for k,v in QueryDict(value).dict().items()},
            'MAX_ENTRIES': int
        })

    for key, value in params.items():
        key = key.upper()
        config[key] = key_coercions[key](value)
    return config

def to_url(config):
    config = deepcopy(config)

    backend = config.pop('BACKEND', None)

    raw_location = config.pop('LOCATION')
    if isinstance(raw_location, six.string_types):
        location = raw_location
    else:
        location = ";".join(raw_location)

    adapted = {
        'scheme': BACKENDS.get(backend, 'external'),
        'hostname': location,
    }

    if 'USERNAME' in config and 'PASSWORD' in config:
        adapted['auth'] = "{USERNAME}:{PASSWORD}@".format(**config)
        del config['USERNAME']
        del config['PASSWORD']
    else:
        adapted['auth'] = ''

    base_url = "{scheme}://{auth}{hostname}/".format(**adapted)

    query = QueryDict('', mutable=True)

    if not backend in BACKENDS:
        query['external_backend'] = backend

    if 'OPTIONS' in config:
        options = QueryDict('', mutable=True)
        options.update(config.pop('OPTIONS'))
        query['options'] = options.urlencode()
    if 'TIMEOUT' in config:
        query['timeout'] = str(config.pop('TIMEOUT'))
    if 'BINARY' in config:
        query['binary'] = 'true' if config.pop('BINARY') else 'false'

    # no coercion for all other keys:
    for key, value in config.items():
        query[key.lower()] = value

    if query:
        return base_url + "?" + query.urlencode()
    else:
        return base_url
