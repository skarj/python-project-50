#!/usr/bin/env python3

from gendiff import cmd
import json


def generate_diff(json1, json2):
    removed = json1.keys() - json2.keys()
    added = json2.keys() - json1.keys()
    same = json2.keys() & json1.keys()
    all = removed | added | same

    result = ['{']
    for k in sorted(all):
        if k in removed:
            result.append(f'  - {k}: {json1[k]}')
        if k in added:
            result.append(f'  + {k}: {json2[k]}')
        if k in same:
            if json1[k] != json2[k]:
                result.append(f'  - {k}: {json1[k]}')
                result.append(f'  + {k}: {json2[k]}')
            else:
                result.append(f'    {k}: {json1[k]}')
    result.append('}')

    return '\n'.join(result)


def main():
    args = cmd.get_args()
    file1 = args.first_file
    file2 = args.second_file

    json1 = json.load(open(file1))
    json2 = json.load(open(file2))

    print(generate_diff(json1, json2))


if __name__ == '__main__':
    main()
