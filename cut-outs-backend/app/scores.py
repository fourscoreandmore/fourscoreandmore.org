from app import app
from natsort import natsorted
from music21 import converter
import json
import operator
import os

def normalizeScorePath(path, subDir=""):
    base_path=app.config["SCORE_PATH"]
    prefixed=os.path.join(subDir, path.strip('./'))
    abs=os.path.join(base_path, prefixed)

    if not os.path.isfile(abs):
        raise ValidationError("File not found: " + prefixed)

    return abs


def list_scores(subDir=""):
    dir = os.path.join(app.config['SCORE_PATH'], subDir)
    index_data = get_score_index(dir)

    return natsorted(index_data.items(), key=operator.itemgetter(1))


def get_score_index(path, reset=False):
    index_filename = os.path.join(path, "scores.json")
    if not reset and os.path.isfile(index_filename):
        with open(index_filename, 'r') as index_handle:
            return json.load(index_handle)

    index = {}
    for filename in os.listdir(path):
        if filename.endswith('.xml') or filename.endswith('.mxl'):
            abspath = os.path.abspath(os.path.join(path, filename))
            score = converter.parse(abspath)
            scoreName = "{} - {}".format(score.metadata.composer, score.metadata.title)
            index[filename] = scoreName

    with open(index_filename, 'w') as index_handle:
        json.dump(index, index_handle)

    return index
