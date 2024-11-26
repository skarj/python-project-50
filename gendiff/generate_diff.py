import os
import json
import yaml

from gendiff.formatters.stylish import format_stylish
from gendiff.formatters.plain import format_plain
from gendiff.formatters.json import format_json


def create_diff(content1, content2):
    all_keys = content1.keys() | content2.keys()

    diff = {}
    for k in all_keys:
        if k not in content2:
            diff[k] = {'value': content1[k], 'state': 'removed'}
        elif k not in content1:
            diff[k] = {'value': content2[k], 'state': 'added'}
        elif isinstance(content1[k], dict) and isinstance(content2[k], dict):
            diff[k] = {'children': create_diff(content1[k], content2[k])}
        elif content1[k] != content2[k]:
            diff[k] = {'value': content1[k], 'state': 'updated', 'new_value': content2[k]}
        else:
            diff[k] = content1[k]
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

    content1 = load_file(file1, file1_format)
    content2 = load_file(file2, file2_format)

    diff = create_diff(content1, content2)

    formatters = {
        'stylish': format_stylish,
        'plain': format_plain,
        'json': format_json
    }

    return formatters[format_name](diff)
