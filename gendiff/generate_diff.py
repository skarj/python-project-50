import argparse
import json


def format_line(key, value, symbol=' ', indent=2):
    indent = ' ' * indent

    if isinstance(value, int):
        value = str(value).lower()

    return f'{indent}{symbol} {key}: {value}'


def compare_objects(json1, json2):
    removed = json1.keys() - json2.keys()
    added = json2.keys() - json1.keys()
    same = json2.keys() & json1.keys()
    all = removed | added | same

    result = ['{']
    for k in sorted(all):
        if k in removed:
            result.append(format_line(k, json1[k], '-'))
        if k in added:
            result.append(format_line(k, json2[k], '+'))
        if k in same:
            if json1[k] != json2[k]:
                result.append(format_line(k, json1[k], '-'))
                result.append(format_line(k, json2[k], '+'))
            else:
                result.append(format_line(k, json1[k]))
    result.append('}')

    return '\n'.join(result)


def get_args():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()

    return args


def generate_diff():
    args = get_args()
    file1 = args.first_file
    file2 = args.second_file

    json1 = json.load(open(file1))
    json2 = json.load(open(file2))

    print(compare_objects(json1, json2))
