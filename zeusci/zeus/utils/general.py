import os


abspath = lambda *p: os.path.abspath(os.path.join(*p))


def lookup_value(obj, value):
    """
    """
    if hasattr(obj, value) or '__' not in value:
        return getattr(obj, value)
    attr, value = value.split('__', 1)
    if not value:
        raise AttributeError("Object %r does NOT have attribute %r" % (obj, attr))
    obj = getattr(obj, attr)
    return lookup_value(obj, value)

