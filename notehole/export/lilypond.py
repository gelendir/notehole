from notehole.music import Rest, Note, Chord

TEMPLATE = r"""
\version "2.18.2"

\relative {start_tone} {{
    {score}
}}

{extra}
"""

def create_lilypond_file(score, filename, extra=""):
    exporter = LilypondExporter()
    exporter.append(score, extra)
    exporter.save(filename)


class LilypondExporter(object):

    TONE_SYMBOLS = {
        0: 'c',
        1: 'd',
        2: 'e',
        3: 'f',
        4: 'g',
        5: 'a',
        6: 'b',
    }

    ACCIDENTAL_SYMBOLS = {
        -2: 'eses',
        -1: 'es',
        0: '',
        1: 'is',
        2: 'isis',
    }

    def __init__(self):
        self.tokens = []
        self.start_tone = None
        self.last_tone = None
        self.extra = ""

    def append(self, score, extra=""):
        self.find_start_tone(score)
        self.tokens.append(self.format_meter(score.meter))
        self.tokens.extend(self.format_item(item) for item in score)
        self.extra += extra

    def find_start_tone(self, score):
        if self.start_tone:
            return

        item_filter = lambda x: isinstance(x, (Note, Chord))
        item = next(filter(item_filter, score))

        if isinstance(item, Note):
            self.start_tone = self.last_tone = item.tone
        elif isinstance(item, Chord):
            self.start_tone = self.last_tone = item.sorted_tones()[0]

    def format_item(self, item):
        if isinstance(item, Rest):
            return self.format_rest(item)
        elif isinstance(item, Note):
            return self.format_note(item)
        elif isinstance(item, Chord):
            return self.format_chord(item)
        else:
            raise Exception('Unknown item: {}'.format(item))

    def format_rest(self, rest):
        duration = self.format_duration(rest.duration)
        return "r{}".format(duration)

    def format_duration(self, duration):
        return "{}{}".format(duration.value, '.' * duration.dots)

    def format_note(self, note):
        octave = self.last_octave(note.tone)
        tone = self.format_tone(note.tone, octave)
        duration = self.format_duration(note.duration)
        return "{}{}".format(tone, duration)

    def last_octave(self, tone):
        octave = self.relative_octave(tone, self.last_tone)
        self.last_tone = tone
        return octave

    def relative_octave(self, high, low):
        delta = high.pitch - low.pitch
        direction = -1 if high.pitch >= low.pitch else 1
        shift = abs(delta) % 7
        extra = abs(delta) // 7 * direction
        if shift:
            return shift // 4 * direction + extra
        return extra

    def format_tone(self, tone, octave=0):
        return "{}{}{}".format(self.TONE_SYMBOLS[tone.position],
                               self.ACCIDENTAL_SYMBOLS[tone.accidental],
                               self.format_octave(octave))

    def format_octave(self, octave):
        if octave > 0:
            return "'" * octave
        elif octave < 0:
            return ',' * abs(octave)
        return ''

    def format_chord(self, chord):
        tones = chord.sorted_tones()

        first_tone = self.format_tone(tones[0], self.last_octave(tones[0]))
        overlaps = zip(tones[:-1], tones[1:])

        tones = [self.format_tone(bottom, self.relative_octave(top, bottom))
                 for top, bottom in overlaps]

        duration = self.format_duration(chord.duration)

        return "<{} {}>{}".format(first_tone, ' '.join(tones), duration)

    def format_meter(self, meter):
        return "\\time {}/{}".format(meter.beats, meter.bar)

    def save(self, filename):
        start_octave = self.start_tone.octave - 3
        start_tone = self.format_tone(self.start_tone, start_octave)
        score = ' '.join(self.tokens)
        rendered = TEMPLATE.format(start_tone=start_tone,
                                   score=score,
                                   extra=self.extra)

        with open(filename, 'w') as f:
            f.write(rendered)
