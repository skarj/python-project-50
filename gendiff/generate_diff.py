import argparse
import os
from gendiff.parser import get_parser, create_diff, format_stylish

SUPPORTED_FORMATS = ['.json', '.yaml', '.yml']


def get_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    return parser.parse_args()


def generate_diff(file1, file2):
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
    result = format_stylish(diff)

    return '\n'.join(result)

