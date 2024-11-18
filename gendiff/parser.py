import json
import yaml


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

    diff = {}
    for k in all:
        if k in removed:
            diff[k] = {
                'value': obj1[k],
                'state': 'removed'
            }
        elif k in added:
            diff[k] = {
                'value': obj2[k],
                'state': 'added'
            }
        elif k in same and obj1[k] != obj2[k]:
            diff[k] = {
                'value': obj1[k],
                'state': 'changed',
                'new_value': obj2[k]
            }
        else:
            diff[k] = {'value': obj1[k]}

    return diff


def render_stylish_line(key, value, symbol=' ', indent=2):
    indent = ' ' * indent

    if isinstance(value, bool):
        value = str(value).lower()

    return f'{indent}{symbol} {key}: {value}'


def format_stylish(diff, indent=1):
    result = ['{']
    for k, v in sorted(diff.items()):
        if 'state' in v:
            if v['state'] == 'removed' or v['state'] == 'changed':
                result.append(render_stylish_line(k, v['value'], '-', indent))
            if v['state'] == 'added':
                result.append(render_stylish_line(k, v['value'], '+', indent))
            if v['state'] == 'changed':
                result.append(render_stylish_line(k, v['new_value'], '+', indent))
        else:
            result.append(render_stylish_line(k, v['value'], ' ', indent))

    result.append('}')

    return result


def compare_objects(obj1, obj2):
    diff = create_diff(obj1, obj2)
    result = format_stylish(diff, 2)

    return '\n'.join(result)
