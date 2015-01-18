
NB_PITCHES = 7
NB_SEMITONES = 12

class Tone(object):

    ACCIDENTALS = {
        -2: 'bb',
        -1: 'b',
        0: '',
        1: '#',
        2: 'X'
    }

    PITCH_NAMES = {
        0: 'c',
        1: 'd',
        2: 'e',
        3: 'f',
        4: 'g',
        5: 'a',
        6: 'b'
    }

    PITCH_SEMITONES = {
        0: 0,
        1: 2,
        2: 4,
        3: 5,
        4: 7,
        5: 9,
        6: 11
    }

    NAMED_PITCHES = {value: key for key, value in PITCH_NAMES.items()}

    def __init__(self, pitch, accidental=0):
        self.pitch = pitch
        self.accidental = accidental

    @classmethod
    def named(cls, name, octave, accidental=0):
        pitch = cls.NAMED_PITCHES[name] + octave * NB_PITCHES
        return cls(pitch, accidental)

    def __repr__(self):
        return "[{}{}{}]".format(self.PITCH_NAMES[self.position],
                                 self.ACCIDENTALS[self.accidental],
                                 self.octave)

    def __hash__(self):
        return self.pitch * 5 + 2 + self.accidental

    def __eq__(self, other):
        return self.pitch == other.pitch and self.accidental == other.accidental

    def pitch_tuple(self):
        return (self.pitch, self.accidental)

    @property
    def octave(self):
        return self.pitch // NB_PITCHES

    @property
    def position(self):
        return self.pitch % NB_PITCHES

    @property
    def semitone(self):
        return (self.octave * NB_SEMITONES
                + self.PITCH_SEMITONES[self.position]
                + self.accidental)

    def flip(self, axis):
        delta = self.pitch - axis.pitch
        return Tone(axis.pitch - delta, -self.accidental)

class Note(object):

    def __init__(self, tone, length, dots=0):
        self.tone = tone
        self.length = length
        self.dots = dots

    @classmethod
    def create(cls, pitch, octave, length, accidental=0, dots=0):
        tone = Tone.named(pitch, octave, accidental)
        return cls(tone, length, dots)

    def __repr__(self):
        tone = repr(self.tone)
        dots = '.' * self.dots if self.dots else ''
        return "<{} {}{}>".format(tone, self.length, dots)

    def flip(self, axis):
        return Note(self.tone.flip(axis),
                    self.length,
                    self.dots)

    def fold(self, axis):
        if self.tone == axis:
            return self
        tones = {self.tone, self.tone.flip(axis)}
        return Chord(tones, self.length, self.dots)


class Chord(object):

    def __init__(self, tones, length, dots=0):
        self.tones = tones
        self.length = length
        self.dots = dots

    def __repr__(self):
        sorted_tones = sorted(self.tones,
                              key=lambda x: x.pitch_tuple(),
                              reverse=True)
        tones = ", ".join(repr(t) for t in sorted_tones)
        return "({})".format(tones)

    def flip(self, axis):
        flipped_tones = {t.flip(axis) for t in self.tones}
        return Chord(flipped_tones,
                     self.length,
                     self.dots)

    def fold(self, axis):
        flipped_tones = {t.flip(axis) for t in self.tones}
        tones = self.tones.union(flipped_tones)
        return Chord(tones, self.length, self.dots)


def reverse_notes(notes):
    return list(reversed(notes))


def vertical_fold(notes):
    return notes + reverse_notes(notes)


def repeated_vertical_fold(notes, repetitions):
    reversed_notes = reverse_notes(notes)
    result = list(notes)
    for r in range(repetitions):
        if r % 2 == 0:
            result.extend(reversed_notes)
        else:
            result.extend(notes)

    return result


def repeated_mobius_fold(notes, repetitions):
    flipped_notes = flip_notes(notes)
    result = list(notes)
    for r in range(repetitions):
        if r % 2 == 0:
            result.extend(flipped_notes)
        else:
            result.extend(notes)

    return result


def flip_notes(notes, axis=None):
    axis = axis or Tone.named('b', 3)
    return [n.flip(axis) for n in notes]


def horizontal_fold(notes, axis=None):
    axis = axis or Tone.named('b', 3)
    return [n.fold(axis) for n in notes]


def rotate_180(notes):
    return flip_notes(reverse_notes(notes))


if __name__ == "__main__":
    pass
