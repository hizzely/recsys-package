import json
import pathlib
from data.ingest import get_and_save_articles_as_json


def articles_from_json(path) -> list:
    file = pathlib.Path(path)

    if not file.exists() or not file.stat().st_size > 0:
        get_and_save_articles_as_json(path)

    with open(path, "r") as read_file:
        return json.load(read_file)
