import argparse
import os
import json
import yaml

SUPPORTED_FORMATS = ['.json', '.yaml']


def get_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    return parser.parse_args()


def format_line(key, value, symbol=' ', indent=2):
    indent = ' ' * indent

    if isinstance(value, int):
        value = str(value).lower()

    return f'{indent}{symbol} {key}: {value}'


def get_format_loader(format):
    def loader(file):
        if format == '.yaml':
            obj = yaml.load(open(file), Loader=yaml.Loader)
        elif format == '.json':
            obj = json.load(open(file))
        else:
            return None

        return obj

    return loader


def compare_objects(obj1, obj2):
    removed = obj1.keys() - obj2.keys()
    added = obj2.keys() - obj1.keys()
    same = obj2.keys() & obj1.keys()
    all = removed | added | same

    result = ['{']
    for k in sorted(all):
        if k in removed:
            result.append(format_line(k, obj1[k], '-'))
        if k in added:
            result.append(format_line(k, obj2[k], '+'))
        if k in same:
            if obj1[k] != obj2[k]:
                result.append(format_line(k, obj1[k], '-'))
                result.append(format_line(k, obj2[k], '+'))
            else:
                result.append(format_line(k, obj1[k]))
    result.append('}')

    return '\n'.join(result)


def generate_diff(file1, file2):
    _, file1_format = os.path.splitext(file1)
    _, file2_format = os.path.splitext(file2)

    for format in [file1_format, file2_format]:
        if format not in SUPPORTED_FORMATS:
            print(f'Error! Unsupported format type: {format}')
            os._exit(1)  # ?

    if file1_format != file2_format:
        print('Error! Both files should be of the same format type')
        os._exit(1)  # ?

    loader = get_format_loader(file1_format)

    if not loader:
        print('Error! Unsupported format type')
        os._exit(1)  # ?

    obj1 = loader(file1)
    obj2 = loader(file2)

    return compare_objects(obj1, obj2)
