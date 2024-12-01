from gendiff.file import get_extention, load_file
from gendiff.formatters.utils import get_formatter
from gendiff.parse import parse_file
from gendiff.states import ADDED, REMOVED, UNCHANGED, UPDATED


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
                diff[key] = create_diff(content1[key], content2[key])
            elif content1[key] != content2[key]:
                diff[key] = {'value': (content1[key], content2[key]), 'state': UPDATED}
            else:
                diff[key] = {'value': content1[key], 'state': UNCHANGED}
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
