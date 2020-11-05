from app import app
from app.indexer import get_lieder_index, get_score_index, get_score_name
from natsort import natsorted
import music21.converter
import music21.musicxml
import operator
import os


def normalizeScorePath(path, subDir="", base_path=None):
    base_path = base_path or app.config["SCORE_PATH"]
    prefixed = os.path.join(subDir, path.strip("./"))
    abs = os.path.join(base_path, prefixed)

    if not os.path.isfile(abs):
        raise ValueError("File not found: " + prefixed)

    return abs


def list_scores(subDir=""):
    dir = os.path.join(app.config["SCORE_PATH"], subDir)
    index_data = get_score_index(dir)

    return natsorted(index_data.items(), key=operator.itemgetter(1))


def list_lieder(require_files=[]):
    dir = app.config["LIEDER_CORPUS_PATH"]
    index_data = get_lieder_index(dir, index_filename=app.config["LIEDER_INDEX_PATH"])

    if len(require_files) > 0:
        for path in list(index_data):
            if not all(elem in index_data[path]["files"] for elem in require_files):
                del index_data[path]

    return natsorted(
        [(item[0], item[1]["name"]) for item in index_data.items()],
        key=operator.itemgetter(1),
    )


def lied_by_path(path):
    dir = app.config["LIEDER_CORPUS_PATH"]
    index_data = get_lieder_index(dir, index_filename=app.config["LIEDER_INDEX_PATH"])

    if path in index_data:
        return index_data[path]

    return None
