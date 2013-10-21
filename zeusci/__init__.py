"""
"""

# VERSION should be a tuple of 3 digits + (optional) string
VERSION = (0, 1, 0)


def get_version(full=True):
    """
    Returns stringified version. Could be for example '1.0.0' or '1.0.0a'.
    """
    version = '.'.join((str(each) for each in VERSION[:3]))
    if full and len(VERSION) > 3:
        version += str(VERSION[3])
    return version


__version__ = get_version()

