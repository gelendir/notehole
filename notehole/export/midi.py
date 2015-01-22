from notehole.music import Note, Rest, Chord
import mido

PIANO = 0

def create_midi_file(score, filename):
    exporter = MidiExporter()
    exporter.append(score)
    exporter.save(filename)


class MidiExporter(object):

    TICK = 24
    FILETYPE = 0

    SEMITONES = {
        0: 0,
        1: 2,
        2: 4,
        3: 5,
        4: 7,
        5: 9,
        6: 11
    }

    def __init__(self, instrument=PIANO):
        self.instrument = instrument
        self.track = mido.MidiTrack()

    def append(self, score):
        self.add_tempo(score.tempo)
        self.add_time_signature(score.meter)
        self.add_instrument(self.instrument)
        self.add_score(score)

    def add_tempo(self, tempo):
        msg = mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo))
        self.track.append(msg)

    def add_time_signature(self, meter):
        msg = mido.MetaMessage('time_signature',
                               numerator=meter.beats,
                               denominator=meter.bar)
        self.track.append(msg)

    def add_instrument(self, instrument):
        msg = mido.Message('program_change', program=instrument)
        self.track.append(msg)

    def add_score(self, score):
        self.track.extend(self.map_score(score))

    def map_score(self, score):
        ticks = 0
        for item in score:
            if isinstance(item, Rest):
                ticks += self.duration_to_ticks(item.duration)
            elif isinstance(item, Note):
                yield from self.map_note(item, ticks)
                ticks = 0
            elif isinstance(item, Chord):
                yield from self.map_chord(item, ticks)
                ticks = 0
            else:
                raise Exception('unknown item {}'.format(item))

    def map_note(self, note, rest_ticks=0):
        midi_note = self.tone_to_midi(note.tone)
        ticks = self.duration_to_ticks(note.duration)
        yield mido.Message('note_on', note=midi_note, time=rest_ticks)
        yield mido.Message('note_off', note=midi_note, time=ticks)

    def tone_to_midi(self, tone):
        return (
            (tone.octave + 1) * 12 +
            self.SEMITONES[tone.position] + tone.accidental
        )

    def duration_to_ticks(self, duration):
        values = [duration.value] + [duration.value * (2**(i+1))
                                     for i in range(duration.dots)]
        ticks = sum(int(self.TICK / (v / 4)) for v in values)
        return ticks

    def map_chord(self, chord, rest_ticks=0):
        notes = [self.tone_to_midi(t) for t in chord.sorted_tones()]
        ticks = self.duration_to_ticks(chord.duration)

        yield mido.Message('note_on', note=notes[0], time=rest_ticks)

        for midi_note in notes[1:]:
            yield mido.Message('note_on', note=midi_note, time=0)

        yield mido.Message('note_off', note=notes[0], time=ticks)

        for midi_note in notes[1:]:
            yield mido.Message('note_off', note=midi_note, time=0)

    def save(self, filename):
        with mido.MidiFile(type=self.FILETYPE, ticks_per_beat=self.TICK) as mid:
            mid.tracks.append(self.track)
            mid.save(filename)
