from gendiff.types import ADDED, NESTED, REMOVED, UNCHANGED, UPDATED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def get_sign(node_type):
    signs = {ADDED: '+', REMOVED: '-', UNCHANGED: ' '}
    return signs.get(node_type, ' ')


def get_indent(depth=1):
    return ' ' * (INDENT * depth - 2)


def format_updated_node(node, depth=1):
    node_key, node_props = node
    value_old, value_new = node_props['value']

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
    node_value = node_props['value']
    sign = get_sign(node_props['type'])

    if isinstance(node_value, dict):
        nodes = {}
        for key, value in node_value.items():
            nodes[key] = {'value': value, 'type': UNCHANGED}

        node_value = format_stylish(nodes, depth + 1)

    return f'{indent}{sign} {node_key}: {stringify(node_value)}'


def format_nested_node(node, depth=1):
    node_key, node_props = node
    node_value = node_props['value']
    node_type = node_props['type']

    return format_node(
        (node_key, {
            "value": format_stylish(node_value, depth + 1),
            "type": node_type
        }), depth
    )


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
