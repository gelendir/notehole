class Rest(object):

    def __init__(self, duration):
        self.duration = duration

    def __repr__(self):
        return "R-{}".format(repr(self.duration))

    def flip(self, axis):
        return self

    def fold(self, axis):
        return self
