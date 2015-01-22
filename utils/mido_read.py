import mido
import sys

filename = sys.argv[1]

mid = mido.MidiFile(filename)
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for message in track:
        print(message)
