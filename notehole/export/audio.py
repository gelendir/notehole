import os
import subprocess

from .midi import create_midi_file
from notehole.util import tmp_filepath

SOUNDFONT_PATH = '/usr/share/soundfonts/FluidR3_GM2-2.sf2'
DEFAULT_BITRATE = 96

def create_wav_file(score, filename):
    with tmp_filepath() as filepath:
        create_midi_file(score, filepath)
        cmd = ['fluidsynth', SOUNDFONT_PATH, filepath, '-F', filename]
        subprocess.check_call(cmd)


def create_mp3_file(score, filename):
    with tmp_filepath() as filepath:
        create_wav_file(score, filepath)
        cmd = ['lame', '-b', str(DEFAULT_BITRATE), '-f', filepath, filename]
        subprocess.check_call(cmd)


