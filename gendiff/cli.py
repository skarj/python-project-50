import argparse

from gendiff.formatters.utils import FORMATTERS


def parse_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        default='stylish',
                        help='set format of output',
                        choices=FORMATTERS.keys())

    return parser.parse_args()
