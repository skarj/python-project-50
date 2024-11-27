import os
import json
import yaml


def load_file(file):
    return open(file, 'r')


def parse_file(file_path):
    _, file_extention = os.path.splitext(file_path)
    if file_extention not in {'.json', '.yaml', '.yml'}:
        raise ValueError(f'Unsupported format type: {file_extention}')
    elif file_extention in {'.yaml', '.yml'}:
        return yaml.safe_load(load_file(file_path))
    else:
        return json.load(load_file(file_path))
