import argparse
import os
import json
import yaml
from gendiff.formatters.stylish import format_stylish

SUPPORTED_FORMATS = ['.json', '.yaml', '.yml']


def get_parser(format):
    def loader(file):
        if format in ['.yaml', 'yml']:
            obj = yaml.load(open(file), Loader=yaml.Loader)
        else:
            obj = json.load(open(file))

        return obj

    return loader


def get_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', default='stylish',
                        help='set format of output', choices=['stylish', 'plain'])

    return parser.parse_args()


def create_diff(obj1, obj2):
    removed = obj1.keys() - obj2.keys()
    added = obj2.keys() - obj1.keys()
    same = obj2.keys() & obj1.keys()
    all = removed | added | same

    diff = {}
    for k in all:
        if k in removed:
            diff[k] = {'value': obj1[k], 'state': 'removed'}
        elif k in added:
            diff[k] = {'value': obj2[k], 'state': 'added'}
        elif k in same and obj1[k] != obj2[k]:
            if isinstance(obj1[k], dict) and isinstance(obj2[k], dict):
                diff[k] = {'children': create_diff(obj1[k], obj2[k])}
            else:
                diff[k] = {
                    'value': obj1[k],
                    'state': 'changed',
                    'new_value': obj2[k]
                }
        else:
            diff[k] = {'value': obj1[k], 'state': 'unchanged'}

    return diff


def generate_diff(file1, file2, format_name='stylish'):
    _, file1_format = os.path.splitext(file1)
    _, file2_format = os.path.splitext(file2)

    for format in [file1_format, file2_format]:
        if format not in SUPPORTED_FORMATS:
            return f'Error! Unsupported format type: {format}'

    file1_parser = get_parser(file1_format)
    file2_parser = get_parser(file2_format)

    object1 = file1_parser(file1)
    object2 = file2_parser(file2)

    diff = create_diff(object1, object2)

    if format_name == 'stylish':
        result = format_stylish(diff)

    return '\n'.join(result)
