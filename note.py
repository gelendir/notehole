import re

from tone import Tone, parse_tone

duration_regex = re.compile(r"\-(\d+)(\.*)$")

def parse_note(text):
    tone = parse_tone(text)
    duration = parse_duration(text)
    return Note(tone, duration)


def parse_duration(text):
    match = duration_regex.search(text)
    length = int(match.group(1))
    dots = len(match.group(2)) if match.group(2) else 0

    return Duration(length, dots)


class Duration(object):

    def __init__(self, value, dots=0):
        self.value = value
        self.dots = dots

    def __repr__(self):
        dots = '.' * self.dots if self.dots else ''
        return "{}{}".format(self.value, dots)


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


class Chord(object):

    def __init__(self, tones, duration):
        self.tones = tones
        self.duration = duration

    def __repr__(self):
        sorted_tones = sorted(self.tones,
                              key=lambda x: x.pitch_tuple(),
                              reverse=True)
        tones = ", ".join(repr(t) for t in sorted_tones)
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

