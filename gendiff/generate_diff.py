import os
import json
import yaml

from gendiff.formatters.stylish import format_stylish
from gendiff.formatters.plain import format_plain
from gendiff.formatters.json import format_json
from gendiff.states import ADDED, UPDATED, REMOVED


def create_diff(content1, content2):
    all_keys = content1.keys() | content2.keys()

    diff = {}
    for key in all_keys:
        if key not in content2:
            diff[key] = {'value': content1[key], 'state': REMOVED}
        elif key not in content1:
            diff[key] = {'value': content2[key], 'state': ADDED}
        elif isinstance(content1[key], dict) and isinstance(content2[key], dict):
            diff[key] = {'children': create_diff(content1[key], content2[key])}
        elif content1[key] != content2[key]:
            diff[key] = {'value': content1[key], 'state': UPDATED, 'new_value': content2[key]}
        else:
            diff[key] = content1[key]
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
