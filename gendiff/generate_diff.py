from gendiff.parse import parse_file
from gendiff.formatters.utils import get_formatter
from gendiff.states import ADDED, UPDATED, REMOVED


def create_diff(content1, content2):
    removed_keys = content1.keys() - content2.keys()
    added_keys = content2.keys() - content1.keys()
    same_keys = content2.keys() & content1.keys()
    all_keys = content1.keys() | content2.keys()

    diff = {}
    for key in all_keys:
        if key in removed_keys:
            diff[key] = {'value': content1[key], 'state': REMOVED}
        elif key in added_keys:
            diff[key] = {'value': content2[key], 'state': ADDED}
        elif key in same_keys:
            if isinstance(content1[key], dict) and isinstance(content2[key], dict):
                diff[key] = {'children': create_diff(content1[key], content2[key])}
            elif content1[key] != content2[key]:
                diff[key] = {'value': content1[key], 'state': UPDATED, 'new_value': content2[key]}
            else:
                diff[key] = content1[key]
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    content1 = parse_file(file_path1)
    content2 = parse_file(file_path2)

    diff = create_diff(content1, content2)
    formatter = get_formatter(format_name)

    return formatter(diff)
