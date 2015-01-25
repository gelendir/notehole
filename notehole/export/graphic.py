import uuid
import tempfile
import os.path
import shutil
import subprocess

from .lilypond import create_lilypond_file

EXTRA = """
\paper {
    indent=0\mm
    line-width=120\mm
    oddFooterMarkup=##f
    oddHeaderMarkup=##f
    bookTitleMarkup = ##f
    scoreTitleMarkup = ##f
}
"""

def create_png_file(score, filename):
    directory = tempfile.mkdtemp()
    ly_filepath = os.path.join(directory, str(uuid.uuid4()))
    png_filepath = os.path.join(directory, str(uuid.uuid4()))

    create_lilypond_file(score, ly_filepath, EXTRA)

    cmd = ['lilypond', '-dbackend=eps', '-dno-gs-load-fonts',
            '-dinclude-eps-fonts', '--png', '-o', png_filepath, ly_filepath]
    subprocess.check_call(cmd)

    shutil.move(png_filepath + '.png', filename)
    shutil.rmtree(directory)
