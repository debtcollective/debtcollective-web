import logging
import os
import re
from types import NoneType


logger = logging.getLogger(__name__)


def get_envconfig(globals_):
    """For use in the settings.py, this function allows any setting to
    be overridden by the process environment.
    """
    for var in globals_.keys():
        if not re.match(r'^[A-Z0-9_]+$', var):
            continue
        if var in os.environ:
            value = os.environ.get(var)
            dest_type = type(globals_[var])
            if dest_type == bool:
                # permit many sensible 'no/false' settings
                value = False if re.match(
                    r'^(f(alse)?|off|0|n(o)?)?$', value, re.I,
                ) else True
            elif dest_type == NoneType:
                value = str(value)
            else:
                # type-preserving assign
                value = dest_type(value)

            globals_[var] = value
