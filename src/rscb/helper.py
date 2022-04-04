import json


def save_dict_as_json(source_dict, save_path):
    with open(save_path, 'w') as out:
        json.dump(source_dict, out)
