from pathlib import Path
import jsonlines
import logging
import music21.converter
import os
import time


def get_score_name(score):
    title = score.metadata.title
    if score.metadata.movementNumber and score.metadata.movementNumber != title:
        title += ": " + score.metadata.movementNumber
    if score.metadata.movementName and score.metadata.movementName != title:
        title += ", " + score.metadata.movementName

    return "{} - {}".format(score.metadata.composer, title)


def get_lieder_index(path, index_filename="/tmp/lieder.jsonl", rebuild=False):
    fp = open(index_filename, "r")
    existing = {}
    index = {}
    with jsonlines.Reader(fp) as reader:
        for data in reader.iter(type=dict, skip_invalid=True):
            if "relative_path" in data:
                existing[data["relative_path"]] = data
                index[data["relative_path"]] = data["name"]

    if not rebuild:
        return index

    fp = open(index_filename, "r+")
    writer = jsonlines.Writer(fp, flush=True, sort_keys=True)
    for score_path in Path(path).rglob("score.mxl"):
        data = {}
        start = time.perf_counter()
        data["abspath"] = os.path.abspath(str(score_path))
        data["relative_path"] = str(score_path.relative_to(path))
        if data["relative_path"] in existing:
            existing_score = existing[data["relative_path"]]
            print("Score already parsed: " + data["relative_path"])
            data["name"] = existing_score["name"]
            data["composer"] = existing_score["composer"]
            data["parse_time"] = existing_score["parse_time"]
        else:
            try:
                score = music21.converter.parse(data["abspath"])
                data["name"] = get_score_name(score)
                data["composer"] = score.metadata.composer
                data["parse_time"] = time.perf_counter() - start
                print(
                    f"Parsed score: "
                    + data["relative_path"]
                    + f' in {data["parse_time"]:0.4f} seconds'
                )
            except Exception as e:
                logging.exception("Failed to parse score: " + data["abspath"])
                continue
            writer.write(data)
        index[data["relative_path"]] = data["name"]

    writer.close()
    fp.close()

    return index
