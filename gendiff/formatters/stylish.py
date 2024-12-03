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
    node_key, node_props = node
    node_value = node_props['value']
    value_old, value_new = node_value

    removed = format_node(
        (node_key, {"value": value_old, "type": REMOVED}), depth
    )
    added = format_node(
        (node_key, {"value": value_new, "type": ADDED}), depth
    )

    return f'{removed}\n{added}'


def format_node(node, depth=1):
    indent = get_indent(depth)

    node_key, node_props = node
    node_type = node_props['type']
    node_value = node_props['value']
    sign = get_sign(node_type)

    if isinstance(node_value, dict):
        node = {}
        for key, value in node_value.items():
            node[key] = {'value': value, 'type': UNCHANGED}

        node_value = format_stylish(node, depth + 1)

    return f'{indent}{sign} {node_key}: {stringify(node_value)}'


def format_nested_node(node, depth=1):
    indent = get_indent(depth)

    node_key, node_props = node
    node_type = node_props['type']
    node_value = node_props['value']
    sign = get_sign(node_type)

    return f'{indent}{sign} {node_key}: {format_stylish(node_value, depth + 1)}'


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

    indent = ' ' * (INDENT * (depth - 1))
    return '{\n' + '\n'.join(result) + f'\n{indent}}}'
