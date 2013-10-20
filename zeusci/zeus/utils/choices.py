
class Choices(object):

    def __init__(self, *args, **kwargs):
        self._choices = {}
        kwargs.update({arg: arg for arg in args})
        for name, value in kwargs.items():
            self._choices[name] = value

    def __getitem__(self, name):
        return self._choices[name]

    def __getattr__(self, name):
        return self[name]

    def as_dict(self):
        return dict(self._choices)

