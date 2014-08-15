from __future__ import absolute_import

import os

from .six.moves.urllib.parse import quote, unquote, urlsplit, urlunsplit, urlencode as original_urlencode

from .datastructures import QueryDict, force_bytes

def resolve_url(url=None, env=None, default_env=None):
    if url is None:
        if env is None:
            env = default_env
        if not env in os.environ:
            return
        return os.environ[env]
    return url

try:
    from django.utils.http import urlencode
except ImportError:
    urlencode = original_urlencode

def delimited(text, delimiter=','):
    """
    Given delimited text, returns a list, excluding
    un-.strip'd zero-length strings.
    "" -> []
    "," -> []
    "a,,b" -> ['a', 'b']
    "a, b" -> ['a', ' b']
    """
    return filter(lambda part: len(part), text.split(delimiter))

def apply_differences(existing, extras, exceptions):
    for exception in exceptions:
        try:
            existing.remove(exception)
        except ValueError:
            print "Unable to remove exception: {0} - it isn't included.".format(exception)
            pass

    for extra in extras:
        existing.append(extra)

_no_default = object()

def from_env(name, default=_no_default, strip_comments=True):
    if default is _no_default:
        value = os.environ[name] # raise if missing
    else:
        value = os.environ.get(name, default)

    if strip_comments and value:
        value = value.split('#', 1)[0].rstrip()

    return value

def bool_str(value):
    return str(value) in ['true', 'True']
