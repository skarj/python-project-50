import os
import json
import yaml

from gendiff.formatters.stylish import format_stylish
from gendiff.formatters.plain import format_plain
from gendiff.formatters.json import format_json


def create_diff(obj1, obj2):
    all_keys = obj1.keys() | obj2.keys()

    diff = {}
    for k in all_keys:
        if k not in obj2:
            diff[k] = {'value': obj1[k], 'state': 'removed'}
        elif k not in obj1:
            diff[k] = {'value': obj2[k], 'state': 'added'}
        elif isinstance(obj1[k], dict) and isinstance(obj2[k], dict):
            diff[k] = {'children': create_diff(obj1[k], obj2[k])}
        elif obj1[k] != obj2[k]:
            diff[k] = {'value': obj1[k], 'state': 'updated', 'new_value': obj2[k]}
        else:
            diff[k] = obj1[k]
    return diff


def load_file(file, file_format):
    with open(file, 'r') as f:
        return yaml.safe_load(f) if file_format in ['.yaml', '.yml'] else json.load(f)


def generate_diff(file1, file2, format_name='stylish'):
    _, file1_format = os.path.splitext(file1)
    _, file2_format = os.path.splitext(file2)

    for format in [file1_format, file2_format]:
        if format not in ['.json', '.yaml', '.yml']:
            return f'Error! Unsupported format type: {format}'

    object1 = load_file(file1, file1_format)
    object2 = load_file(file2, file2_format)

    diff = create_diff(object1, object2)

    formatters = {
        'stylish': format_stylish,
        'plain': format_plain,
        'json': format_json
    }

    result = formatters[format_name](diff)
    string = '\n'.join(result) if format_name != 'json' else result

    return string
