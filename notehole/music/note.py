import re

from .tone import Tone, parse_tone
from .duration import Duration, parse_duration
from .rest import Rest
from .chord import Chord

def parse_note(text):
    duration = parse_duration(text)
    if text[0].lower() == "r":
        return Rest(duration)

    tone = parse_tone(text)
    return Note(tone, duration)


class Note(object):

    def __init__(self, tone, duration):
        self.tone = tone
        self.duration = duration

    def __repr__(self):
        tone = repr(self.tone)
        duration = repr(self.duration)
        return "{}-{}".format(tone, duration)

    def flip(self, axis):
        return Note(self.tone.flip(axis),
                    self.duration)

    def fold(self, axis):
        if self.tone == axis:
            return self
        tones = {self.tone, self.tone.flip(axis)}
        return Chord(tones, self.duration)
