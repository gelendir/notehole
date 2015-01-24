import re

NB_PITCHES = 7
DEFAULT_OCTAVE = 3

ACCIDENTALS = {
    -2: 'bb',
    -1: 'b',
    0: '',
    1: '#',
    2: 'X'
}

PITCHES = {
    0: 'C',
    1: 'D',
    2: 'E',
    3: 'F',
    4: 'G',
    5: 'A',
    6: 'B'
}

NAMED_PITCHES = {value: key for key, value in PITCHES.items()}
NAMED_ACCIDENTALS = {value: key for key, value in ACCIDENTALS.items()}

tone_regex = re.compile(r"^([a-gA-G])(([bX#]|bb)?)(\d?)")


def parse_tone(text):
    match = tone_regex.match(text)
    name = match.group(1).upper()
    accidental = match.group(2) or ''
    octave = int(match.group(4)) if match.group(4) else DEFAULT_OCTAVE

    pitch = octave * NB_PITCHES + NAMED_PITCHES[name]
    accidental = NAMED_ACCIDENTALS[accidental]

    return Tone(pitch, accidental)


class Tone(object):

    def __init__(self, pitch, accidental=0):
        self.pitch = pitch
        self.accidental = accidental

    @classmethod
    def with_octave(cls, pitch, octave, accidental=0):
        return cls(octave * 7 + pitch, accidental)

    def __repr__(self):
        return "{}{}{}".format(PITCHES[self.position],
                               ACCIDENTALS[self.accidental],
                               self.octave)

    def __hash__(self):
        return self.pitch * 5 + 2 + self.accidental

    def __eq__(self, other):
        return self.pitch == other.pitch and self.accidental == other.accidental

    @property
    def octave(self):
        return self.pitch // NB_PITCHES

    @property
    def position(self):
        return self.pitch % NB_PITCHES

    def pitch_tuple(self):
        return (self.pitch, self.accidental)

    def flip(self, axis):
        delta = self.pitch - axis.pitch
        return Tone(axis.pitch - delta, -self.accidental)
