import argparse
import os
import json
import yaml


def get_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()

    return args


def format_line(key, value, symbol=' ', indent=2):
    indent = ' ' * indent

    if isinstance(value, int):
        value = str(value).lower()

    return f'{indent}{symbol} {key}: {value}'


def get_loader(format):
    def loader(file):
        if format == '.yaml':
            obj = yaml.load(open(file), Loader=yaml.Loader)
        elif format == '.json':
            obj = json.load(open(file))
        else:
            return None  # TODO: decide

        return obj

    return loader


def generate_diff(file1, file2):
    _, format1 = os.path.splitext(file1)
    _, format2 = os.path.splitext(file2)

    if format1 == format2:
        loader = get_loader(format1)
    else:
        print('Error: Both files must of the same type')
        os._exit(1)  # TODO: decide

    obj1 = loader(file1)
    obj2 = loader(file2)

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
