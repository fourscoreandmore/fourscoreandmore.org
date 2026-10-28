"""Write sample scores for scripts/render-scores.js: Bach chorales from the
music21 corpus with chorale exercises made from them, and lieder exercises
from any Lieder Corpus scores given.

    uv run python scripts/make-sample-scores.py OUT_DIR [LIED.mxl ...]
"""

import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# The routes need the When-in-Rome romanUmpire module; the exercises don't.
sys.modules.setdefault("app.romanUmpire", types.ModuleType("app.romanUmpire"))

from music21 import corpus  # noqa: E402

from app import exercises  # noqa: E402

out = os.path.abspath(sys.argv[1])
os.makedirs(out, exist_ok=True)

for name in ["bach/bwv66.6", "bach/bwv269"]:
    chorale = os.path.join(out, name.replace("/", "_") + ".mxl")
    corpus.parse(name).write("mxl", fp=chorale)
    print(chorale)
    for short in (False, True):
        for _, path in exercises.ChoraleExercise(chorale, shortScore=short).write(directory=out):
            print(path)

for lied in sys.argv[2:]:
    for options in ({}, {"leaveBassLine": True, "addition": "chordHints"}):
        for _, path in exercises.LiedExercise(lied, **options).write(directory=out):
            print(path)
