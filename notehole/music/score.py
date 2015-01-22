from .meter import Meter

COMMON_METER = Meter(4, 4)

class Score(object):

    def __init__(self, meter=None, tempo=120, items=None):
        self.meter = meter or COMMON_METER
        self.tempo = tempo
        self.items = items or []

    def __iter__(self):
        yield from self.items

    def __repr__(self):
        meter = repr(self.meter)
        items = repr(self.items)
        return "<Score {meter} @ {tempo}: {items}>".format(meter=meter,
                                                           tempo=self.tempo,
                                                           items=items)
