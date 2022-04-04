import json


def save_as_json(source, save_path):
    with open(save_path, 'w') as out:
        json.dump(source, out)
