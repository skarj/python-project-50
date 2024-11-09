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


def render_line(key, value, symbol=' ', indent=2):
    indent = ' ' * indent

    if isinstance(value, int):
        value = str(value).lower()

    return f'{indent}{symbol} {key}: {value}'


def compare_objects(obj1, obj2):
    removed = obj1.keys() - obj2.keys()
    added = obj2.keys() - obj1.keys()
    same = obj2.keys() & obj1.keys()
    all = removed | added | same

    result = ['{']
    for k in sorted(all):
        if k in removed:
            result.append(render_line(k, obj1[k], '-'))
        if k in added:
            result.append(render_line(k, obj2[k], '+'))
        if k in same:
            if obj1[k] != obj2[k]:
                result.append(render_line(k, obj1[k], '-'))
                result.append(render_line(k, obj2[k], '+'))
            else:
                result.append(render_line(k, obj1[k]))
    result.append('}')

    return '\n'.join(result)
