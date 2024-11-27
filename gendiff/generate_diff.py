from gendiff.parse import parse_file
from gendiff.formatters.utils import get_formatter
from gendiff.states import ADDED, UPDATED, REMOVED, UNCHANGED


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
            diff[key] =  {'value': content1[key], 'state': UNCHANGED}
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    content1 = parse_file(file_path1)
    content2 = parse_file(file_path2)

    diff = create_diff(content1, content2)
    formatter = get_formatter(format_name)

    return formatter(diff)
