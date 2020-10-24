from pathlib import Path
import jsonlines
import logging
import os
import time


def get_score_name(score):
    title = score.metadata.title
    if score.metadata.movementNumber and score.metadata.movementNumber != title:
        title += ": " + score.metadata.movementNumber
    if score.metadata.movementName and score.metadata.movementName != title:
        title += ", " + score.metadata.movementName

    return "{} - {}".format(score.metadata.composer, title)


def clean_path(path):
    return str(path).replace("_", " ").strip()


def get_lieder_index(path, index_filename="/tmp/lieder.jsonl", rebuild=False):
    fp = open(index_filename, "r")
    existing = {}
    with jsonlines.Reader(fp) as reader:
        for data in reader.iter(type=dict, skip_invalid=True):
            existing[data["relative_path"]] = data["name"]

    if not rebuild:
        return existing

    index = {}
    fp = open(index_filename, "w")
    writer = jsonlines.Writer(fp, flush=True, sort_keys=True)
    for score_path in Path(path).rglob("score.mxl"):
        data = {}
        data["relative_path"] = str(score_path.relative_to(path))
        data["title"] = clean_path(score_path.parent.name)
        data["collection"] = clean_path(score_path.parent.parent.name)
        data["composer"] = clean_path(score_path.parent.parent.parent.name)
        data["name"] = " - ".join(s for s in [data["composer"], data["collection"], data["title"]] if len(s) > 0)
        index[data["relative_path"]] = data["name"]
        writer.write(data)
        print("Indexed score: " + data["relative_path"])

    print("Indexed " + str(len(index)) + " scores")

    writer.close()
    fp.close()

    return index
