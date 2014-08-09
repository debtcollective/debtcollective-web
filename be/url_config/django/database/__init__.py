# -*- coding: utf-8 -*-
from __future__ import absolute_import
from url_config.utils import QueryDict, resolve_url



import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

DEFAULT_ENV = 'DATABASE_URL'

SCHEMES = {
    'postgres': 'django.db.backends.postgresql_psycopg2',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'external': None # special-case to use querystring param instead.
}

ENGINES = {engine:scheme for scheme, engine in SCHEMES.items()}

for scheme in SCHEMES:
    # Register database schemes in URLs.
    urlparse.uses_netloc.append(scheme)

def from_url(url=None, engine=None, env=None):
    """Parses a database URL.

    If `url` is not provided, the `DEFAULT_ENV` environment variable
    will be used instead. (DEFAULT_ENV is 'DATABASE_URL' by default.)

    If `engine` is provided, it will be used in preference to the
      URL's scheme for selecting `DATABASES` `ENGINE`.

    engine is for compatibility with dj-django-url.
    external:// and ?external_engine are recommended instead.
    """

    url = resolve_url(url, env, DEFAULT_ENV)

    if url is None:
        return

    if url == 'sqlite://:memory:':
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {
            'ENGINE': SCHEMES['sqlite'],
            'NAME': ':memory:'
        }
        # note: no other settings are required for sqlite

    # otherwise parse the url as normal
    config = {}

    url = urlparse.urlparse(url)

    # Remove query strings.
    path = url.path[1:]

    # if we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Update with environment configuration.
    config.update({
        'NAME': path,
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port or '',
    })

    params = QueryDict(url.query, mutable=True)

    if engine:
        config['ENGINE'] = engine
    elif url.scheme == 'external':
        # deal with querydict.get, which returns [''] rather than ''
        config['ENGINE'] = params['external_engine']
        params.pop('external_engine')
    elif url.scheme in SCHEMES:
        config['ENGINE'] = SCHEMES[url.scheme]

    if params:
        config['OPTIONS'] = params

    return config

# dj-database-url compatibility
parse = from_url

def help():
    pass

def to_url(config):
    config = config.copy()
    original_engine = config['ENGINE']
    scheme = ENGINES.get(original_engine, 'external')
    params = QueryDict('', mutable=True)
    params.update(config.get('OPTIONS', {}))

    if scheme == 'external':
        config['SCHEME'] = scheme
        params['external_engine'] = original_engine
    else:
        config['SCHEME'] = scheme

    url = "{SCHEME}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**config)
    if params:
        url += "?" + params.urlencode()
    return url
