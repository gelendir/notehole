import tempfile
import os

from contextlib import contextmanager

@contextmanager
def tmp_filepath():
    fd, filepath = tempfile.mkstemp()
    os.close(fd)
    yield filepath
    os.remove(filepath)
