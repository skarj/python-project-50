import json
import yaml
from collections import defaultdict


def get_parser(format):
    def loader(file):
        if format in ['.yaml', 'yml']:
            obj = yaml.load(open(file), Loader=yaml.Loader)
        else:
            obj = json.load(open(file))

        return obj

    return loader


def create_diff(obj1, obj2):
    removed = obj1.keys() - obj2.keys()
    added = obj2.keys() - obj1.keys()
    same = obj2.keys() & obj1.keys()
    all = removed | added | same

    diff = defaultdict(dict)
    for k in all:
        if k in removed:
            diff["removed"].update({k: obj1[k]})
        elif k in added:
            diff["added"].update({k: obj2[k]})
        elif k in same and obj1[k] != obj2[k]:
            diff["removed"].update({k: obj1[k]})
            diff["added"].update({k: obj2[k]})
        else:
            diff["unchanged"].update({k: obj1[k]})

    return diff


def render_stylish_line(key, value, symbol=' ', indent=2):
    indent = ' ' * indent

    if isinstance(value, bool):
        value = str(value).lower()

    return f'{indent}{symbol} {key}: {value}'


def format_stylish(diff, indent=1):
    all_keys = set(key for sub_dict in diff.values() for key in sub_dict.keys())

    result = ['{']
    for k in sorted(all_keys):
        if k in diff['removed']:
            result.append(render_stylish_line(k, diff['removed'][k], '-'))
        if k in diff['added']:
            result.append(render_stylish_line(k, diff['added'][k], '+'))
        if k in diff['unchanged']:
            result.append(render_stylish_line(k, diff['unchanged'][k]))
    result.append('}')

    return result


def compare_objects(obj1, obj2):
    diff = create_diff(obj1, obj2)
    result = format_stylish(diff, 2)

    return '\n'.join(result)
