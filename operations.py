import itertools
from tone import Tone

B_AXIS = Tone(27)


def reverse_notes(notes):
    return tuple(reversed(notes))


def flip_notes(notes, axis=None):
    axis = axis or B_AXIS
    return tuple(n.flip(axis) for n in notes)


def vertical_fold(notes):
    return itertools.chain(notes, reverse_notes(notes))


def horizontal_fold(notes, axis=None):
    axis = axis or B_AXIS
    return tuple(n.fold(axis) for n in notes)


def repeated_vertical_fold(notes, repetitions):
    cycle = itertools.cycle((notes, reverse_notes(notes)))
    return _repeat_cycle(cycle, repetitions)


def _repeat_cycle(cycle, repetitions):
    repeats = itertools.islice(cycle, repetitions)
    return itertools.chain.from_iterable(repeats)


def repeated_mobius_fold(notes, repetitions):
    cycle = itertools.cycle((notes, flip_notes(notes)))
    return _repeat_cycle(cycle, repetitions)


def rotate_180(notes):
    return flip_notes(reverse_notes(notes))
