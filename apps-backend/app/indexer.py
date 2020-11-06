from pathlib import Path
import json
import jsonlines
import logging
import os
import xml.etree


def get_score_name(score):
    title = score.metadata.title
    if score.metadata.movementNumber and score.metadata.movementNumber != title:
        title += ": " + score.metadata.movementNumber
    if score.metadata.movementName and score.metadata.movementName != title:
        title += ", " + score.metadata.movementName

    return "{} - {}".format(score.metadata.composer, title)


def clean_path(path):
    return str(path).replace("_", " ").strip()


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
            except:
                logging.exception("Failed to parse score: " + abspath)

    with open(index_filename, "w") as index_handle:
        json.dump(index, index_handle)

    return index


def get_lieder_index(path, index_filename="/tmp/lieder.jsonl", rebuild=False):
    fp = open(index_filename, "r")
    existing = {}
    with jsonlines.Reader(fp) as reader:
        for data in reader.iter(type=dict, skip_invalid=True):
            if "relative_dir" in data:
                existing[data["relative_dir"]] = data

    if len(existing) > 0 and not rebuild:
        return existing

    index = {}
    fp = open(index_filename, "w")
    writer = jsonlines.Writer(fp, flush=True, sort_keys=True)
    path=os.path.abspath(path)
    for score_path in Path(path).rglob("score.mxl"):
        data = {}
        data["relative_path"] = str(score_path.relative_to(path))
        data["title"] = clean_path(score_path.parent.name)
        data["collection"] = clean_path(score_path.parent.parent.name)
        data["composer"] = clean_path(score_path.parent.parent.parent.name)
        data["name"] = " - ".join(
            s
            for s in [data["composer"], data["collection"], data["title"]]
            if len(s) > 0
        )
        data["dir"] = str(score_path.parent)
        data["relative_dir"] = str(score_path.parent.relative_to(path))
        data["files"] = os.listdir(str(score_path.parent))
        index[data["relative_dir"]] = data
        writer.write(data)
        print("Indexed score: " + data["relative_path"])

    print("Indexed " + str(len(index)) + " scores")

    writer.close()
    fp.close()

    return index
