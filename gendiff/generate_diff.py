from gendiff.file import get_extention, load_file
from gendiff.formatters.utils import get_formatter
from gendiff.parse import parse_file
from gendiff.types import ADDED, NESTED, REMOVED, UNCHANGED, UPDATED


def create_diff(content1, content2):
    removed_keys = content1.keys() - content2.keys()
    added_keys = content2.keys() - content1.keys()
    same_keys = content2.keys() & content1.keys()
    all_keys = content1.keys() | content2.keys()

    diff = {}
    for key in all_keys:
        if key in removed_keys:
            value = content1[key]
            diff[key] = {
                'value': value,
                'type': REMOVED
            }
        elif key in added_keys:
            value = content2[key]
            diff[key] = {
                'value': value,
                'type': ADDED
            }
        elif key in same_keys:
            value1 = content1[key]
            value2 = content2[key]
            if isinstance(value1, dict) and isinstance(value2, dict):
                diff[key] = {
                    'value': create_diff(value1, value2),
                    'type': NESTED
                }
            elif value1 != value2:
                diff[key] = {
                    'value': (value1, value2),
                    'type': UPDATED
                }
            else:
                diff[key] = {
                    'value': value1,
                    'type': UNCHANGED
                }
    return diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    file1_extention = get_extention(file_path1)
    file2_extention = get_extention(file_path2)

    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    content1 = parse_file(file1, file1_extention)
    content2 = parse_file(file2, file2_extention)

    diff = create_diff(content1, content2)
    formatter = get_formatter(format_name)

    return formatter(diff)
