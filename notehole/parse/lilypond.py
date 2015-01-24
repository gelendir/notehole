import abc

import ly.document

from fractions import Fraction
from ly.music import document as music_document, items
from notehole.music import Score, Note, Duration, Tone, Chord, Rest, Meter

BASE_OCTAVE = 3

def parse_lilypond(text):
    converters = {items.Note: NoteConverter(),
                  items.Chord: ChordConverter(),
                  items.Rest: RestConverter()}
    parser = LilypondParser(converters)
    return parser.parse(text)


class ParseError(Exception):
    pass


class Filter(metaclass=abc.ABCMeta):

    def __init__(self, items, converters):
        self.items = items
        self.converters = converters

    @abc.abstractmethod
    def __iter__(self):
        pass


class MusicFilter(Filter):

    IGNORE = (items.TimeSignature,
              )

    def __iter__(self):
        item_classes = tuple(self.converters.keys())
        for item in self.items:
            if isinstance(item, self.IGNORE):
                continue
            elif not isinstance(item, item_classes):
                raise ParseError("{} is not supported".format(item.token))
            yield item


class AbsoluteOctaveFilter(Filter):

    def __iter__(self):
        for item in self.items:
            converter = self.converters[item.__class__]
            converted_item = converter.absolute_octave(item)
            yield converted_item


class RelativeOctaveFilter(Filter):

    def __init__(self, items, converters, first_pitch):
        super().__init__(items, converters)
        self.first_pitch = first_pitch

    def __iter__(self):
        last_pitch = self.first_pitch
        for item in self.items:
            converter = self.converters[item.__class__]
            converted_item, pitch = converter.relative_octave(item, last_pitch)
            yield converted_item
            last_pitch = pitch


class Converter(metaclass=abc.ABCMeta):

    DURATIONS = (Fraction(1, 1),
                 Fraction(1, 2),
                 Fraction(1, 4),
                 Fraction(1, 8),
                 Fraction(1, 16),
                 Fraction(1, 32),
                 Fraction(1, 64),
                 Fraction(1, 128),
                 )

    @abc.abstractmethod
    def convert_item(self, item):
        pass

    @abc.abstractmethod
    def relative_octave(self, item, last_pitch):
        pass

    @abc.abstractmethod
    def absolute_octave(self, item):
        pass

    def convert_pitch(self, pitch):
        return Tone.with_octave(pitch.note,
                                pitch.octave,
                                int(pitch.alter * 2))

    def convert_duration(self, duration):
        base = next(i for i in self.DURATIONS if duration[0] // i == 1)
        dots = self.calculate_dots(base, duration[0])
        return Duration(base.denominator, dots)

    def calculate_dots(self, base, duration):
        dots = 0
        factor = base / 2
        remainder = duration % base
        while remainder > 0 and factor >= self.DURATIONS[-1]:
            remainder -= factor
            dots += 1
            factor /= 2
        return dots


class NoteConverter(Converter):

    def relative_octave(self, note, last_pitch):
        note.pitch.makeAbsolute(last_pitch)
        return note, note.pitch

    def absolute_octave(self, note):
        note.pitch.octave += BASE_OCTAVE
        return note

    def convert_item(self, note):
        tone = self.convert_pitch(note.pitch)
        duration = self.convert_duration(note.duration)
        return Note(tone, duration)


class ChordConverter(Converter):

    def relative_octave(self, chord, last_pitch):
        pitches = [n.pitch for n in chord.find_children(items.Note)]

        tops = [last_pitch] + pitches[:-1]
        bottoms = pitches

        for top, bottom in zip(tops, bottoms):
            bottom.makeAbsolute(top)

        return chord, pitches[0]

    def absolute_octave(self, chord):
        pitches = (n.pitch for n in chord.find_children(items.Note))
        for pitch in pitches:
            pitch.octave += BASE_OCTAVE
        return chord

    def convert_item(self, chord):
        pitches = (n.pitch for n in chord.find_children(items.Note))
        tones = {self.convert_pitch(p) for p in pitches}
        duration = self.convert_duration(chord.duration)
        return Chord(tones, duration)


class RestConverter(Converter):

    def relative_octave(self, rest, last_pitch):
        return rest, last_pitch

    def absolute_octave(self, rest):
        return rest

    def convert_item(self, rest):
        duration = self.convert_duration(rest.duration)
        return Rest(duration)


class LilypondParser(object):

    def __init__(self, converters):
        self.converters = converters

    def parse(self, text):
        document = ly.document.Document(text)
        music = music_document(document)
        return self.parse_music(music)

    def parse_music(self, music):
        relative_pitch = self.find_relative_pitch(music)
        music_list = self.find_music_list(music)
        music_filter = self.build_filters(music_list, relative_pitch)
        time_signature = self.find_time_signature(music)
        return self.build_score(music_filter, time_signature)

    def find_music_list(self, music):
        music_list = music.find_child(items.MusicList)
        if not music_list:
            raise ParseError("could not find any music block")
        return music_list

    def find_relative_pitch(self, music):
        relative_block = music.find_child(items.Relative)
        if not relative_block:
            return None

        relative_note = relative_block.find_child(items.Note, 1)
        if relative_note:
            pitch = relative_note.pitch.copy()
            pitch.octave += BASE_OCTAVE
            return pitch

        first_note = relative_block.find_child(items.Note)
        if not first_note:
            raise ParseError("no music in relative block")

        pitch = first_note.pitch.copy()
        pitch.octave += BASE_OCTAVE - pitch.octave
        return pitch

    def build_filters(self, music_list, relative_pitch=None):
        music_filter = MusicFilter(music_list, self.converters)
        if relative_pitch:
            return RelativeOctaveFilter(music_filter,
                                        self.converters,
                                        relative_pitch)
        return AbsoluteOctaveFilter(music_filter, self.converters)

    def find_time_signature(self, music):
        return music.find_child(items.TimeSignature)

    def build_score(self, items, time_signature=None):
        meter = self.convert_time_signature(time_signature) if time_signature else None
        converted_items = tuple(self.convert_item(item) for item in items)
        return Score(items=converted_items, meter=meter)

    def convert_time_signature(self, time_signature):
        beats = time_signature.numerator()
        bar = time_signature.fraction().denominator
        return Meter(beats, bar)

    def convert_item(self, item):
        converter = self.converters.get(item.__class__)
        return converter.convert_item(item)
