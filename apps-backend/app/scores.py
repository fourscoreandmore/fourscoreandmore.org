from app import app
from app.indexer import get_lieder_index, get_score_name
from natsort import natsorted
import music21.converter
import music21.musicxml
import xml.etree
import json
import logging
import operator
import os
import time


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


def get_score_index(path, reset=False):
    index_filename = os.path.join(path, "scores.json")
    if not reset and os.path.isfile(index_filename):
        with open(index_filename, "r") as index_handle:
            return json.load(index_handle)

    index = {}
    for filename in os.listdir(path):
        if filename.endswith(".xml") or filename.endswith(".mxl"):
            abspath = os.path.abspath(os.path.join(path, filename))
            try:
                score = music21.converter.parse(abspath)
                index[filename] = get_score_name(score)
            except xml.etree.ElementTree.ParseError as e:
                logging.error("Failed to parse score: " + abspath)
            except music21.musicxml.xmlToM21.MusicXMLImportException as e:
                logging.error("Failed to parse score: " + abspath)

    with open(index_filename, "w") as index_handle:
        json.dump(index, index_handle)

    return index


def list_lieder():
    dir = app.config["LIEDER_CORPUS_PATH"]
    index_data = get_lieder_index(dir, index_filename=app.config["LIEDER_INDEX_PATH"])

    return natsorted(index_data.items(), key=operator.itemgetter(1))
