class Meter(object):

    def __init__(self, beats, bar):
        self.beats = beats
        self.bar = bar

    def __repr__(self):
        return "{}/{}".format(self.beats, self.bar)
