from gendiff.types import ADDED, REMOVED, UPDATED, UNCHANGED, NESTED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def get_sign(node_type):
    if node_type == ADDED:
        return '+'
    elif node_type == REMOVED:
        return '-'
    return ' '


def get_indent(depth=1):
    return ' ' * (INDENT * depth - 2)


def format_updated_node(node, depth=1):
    key, prop = node
    value = prop['value']
    value_old, value_new = value

    removed = format_node((key, {"value": value_old, "type": REMOVED}), depth)
    added = format_node((key, {"value": value_new, "type": ADDED}), depth)

    return f'{removed}\n{added}'


def format_node(node, depth=1):
    indent = get_indent(depth)

    key, val = node
    type = val['type']
    value = val['value']
    sign = get_sign(type)

    if isinstance(value, dict):
        new_node = {}
        for k, v in value.items():
            new_node[k] = {'value': v, 'type': UNCHANGED}

        value = format_stylish(new_node, depth + 1)

    return f'{indent}{sign} {key}: {stringify(value)}'


def format_nested_node(node, depth=1):
    indent = get_indent(depth)

    key, prop = node
    node_type = prop['type']
    value = prop['value']
    sign = get_sign(node_type)

    return f'{indent}{sign} {key}: {format_stylish(value, depth + 1)}'


def format_stylish(diff, depth=1):
    result = []
    for node in sorted(diff.items()):
        _, value = node
        node_type = value['type']
        if node_type == NESTED:
            result.append(format_nested_node(node, depth))
        elif node_type == UPDATED:
            result.append(format_updated_node(node, depth))
        else:
            result.append(format_node(node, depth))

    indent = ' ' * (INDENT * (depth - 1))  # TODO
    return '{\n' + '\n'.join(result) + f'\n{indent}}}'
