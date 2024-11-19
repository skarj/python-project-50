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
            if isinstance(obj1[k], dict) and isinstance(obj2[k], dict):
                diff[k] = {
                    'children': create_diff(obj1[k], obj2[k])
                }
            else:
                diff[k] = {
                    'value': obj1[k],
                    'state': 'changed',
                    'new_value': obj2[k]
                }
        else:
            diff[k] = {
                'value': obj1[k],
                'state': 'unchanged',
            }

    return diff


def format_json(json, depth=1, diff_symbol=' ',
                indent_symbol=' ', indent_size=4):

    def parse(data, result, depth, diff_symbol):
        indent = indent_symbol * (indent_size * depth - 2)
        for k, v in data.items():
            if isinstance(v, dict):
                result.append(f'{indent}{diff_symbol} {k}: {{')
                parse(v, result, depth + 1, ' ')
                result.append(f'{indent}  }}')
            else:
                if isinstance(v, bool):
                    v = str(v).lower()
                if v is None:
                    v = 'null'
                result.append(f'{indent}{diff_symbol} {k}: {v}'.rstrip())
        return result

    result = []
    result = parse(json, result, depth, diff_symbol)

    return result


def format_stylish(diff, indent_size=4):

    def format(data, result, depth=1):
        indent = ' ' * (indent_size * depth - 2)

        for k, v in sorted(data.items()):
            if 'children' in v:
                result.append(f'{indent}  {k}: {{')
                format(v['children'], result, depth + 1)
                result.append(f'{indent}  }}')
            elif v['state'] == 'removed':
                result.extend(format_json({k: v['value']}, depth, '-'))
            elif v['state'] == 'added':
                result.extend(format_json({k: v['value']}, depth, '+'))
            elif v['state'] == 'changed':
                result.extend(format_json({k: v['value']}, depth, '-'))
                result.extend(format_json({k: v['new_value']}, depth, '+'))
            elif v['state'] == 'unchanged':
                result.extend(format_json({k: v['value']}, depth, ' '))

        return result

    result = ['{']
    result = format(diff, result)
    result.append('}')

    return result


def compare_objects(obj1, obj2):
    diff = create_diff(obj1, obj2)
    result = format_stylish(diff)

    return '\n'.join(result)
