import itertools
from notehole.music import Tone

B_AXIS = Tone(34)


def reverse(items):
    return tuple(reversed(items))


def flip(items, axis=None):
    axis = axis or B_AXIS
    return tuple(i.flip(axis) for i in items)


def rotate_180(items):
    return flip(reverse(items))


def vertical_fold(items, repeats=1):
    cycle = itertools.cycle((items, reverse(items)))
    return _repeat_fold(cycle, repeats)


def horizontal_fold(items, axis=None):
    axis = axis or B_AXIS
    return tuple(i.fold(axis) for i in items)


def mobius_fold(items, repeats=1):
    cycle = itertools.cycle((items, flip(items)))
    return _repeat_fold(cycle, repeats)


def _repeat_fold(cycle, repeats):
    repeats = itertools.islice(cycle, repeats + 1)
    return itertools.chain.from_iterable(repeats)
