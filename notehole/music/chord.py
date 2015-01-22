class Chord(object):

    def __init__(self, tones, duration):
        self.tones = tones
        self.duration = duration

    def __repr__(self):
        tones = ", ".join(repr(t) for t in self.sorted_tones())
        duration = repr(self.duration)
        return "<{}-{}>".format(tones, duration)

    def flip(self, axis):
        flipped_tones = {t.flip(axis) for t in self.tones}
        return Chord(flipped_tones,
                     self.duration)

    def fold(self, axis):
        flipped_tones = {t.flip(axis) for t in self.tones}
        tones = self.tones.union(flipped_tones)
        return Chord(tones, self.duration)

    def sorted_tones(self):
        return sorted(self.tones,
                      key=lambda x: x.pitch_tuple(),
                      reverse=True)
