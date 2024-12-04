from gendiff.models import Node
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
    value_old, value_new = node.value
    removed = format_node(
        Node(node.key, value_old, REMOVED), depth
    )
    added = format_node(
        Node(node.key, value_new, ADDED), depth
    )

    return f'{removed}\n{added}'


def format_node(node, depth=1):
    indent = get_indent(depth)
    sign = get_sign(node.type)
    node_value = node.value

    if isinstance(node_value, list):
        nodes = []
        for node in node_value:
            nodes.append(Node(node.key, node.value, UNCHANGED))

        node_value = format_stylish(nodes, depth + 1)

    return f'{indent}{sign} {node.key}: {stringify(node_value)}'


def format_nested_node(node, depth=1):
    return format_node(
        Node(node.key, format_stylish(node.value, depth + 1), node.type), depth
    )


def format_stylish(diff, depth=1):
    result = []
    for node in sorted(diff):
        if node.type == NESTED:
            result.append(format_nested_node(node, depth))
        elif node.type == UPDATED:
            result.append(format_updated_node(node, depth))
        else:
            result.append(format_node(node, depth))

    indent = ' ' * (INDENT * (depth - 1))
    return '{\n' + '\n'.join(result) + f'\n{indent}}}'
