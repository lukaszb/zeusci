import jsonfield


def bytes2str(obj):
    """
    Recursively changes bytes into str for given object.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = bytes2str(value)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            obj[i] = bytes2str(value)
    elif isinstance(obj, bytes):
        return obj.decode('utf8')
    return obj


class JSONField(jsonfield.JSONField):

    def get_db_prep_value(self, value, connection, prepared=False):
        value = bytes2str(value)
        return super().get_db_prep_value(value, connection, prepared)
