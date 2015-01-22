import re

duration_regex = re.compile(r"\-(\d+)(\.*)$")

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
