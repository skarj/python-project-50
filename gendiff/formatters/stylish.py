from gendiff.diff import ADDED, NESTED, REMOVED, UNCHANGED, UPDATED, Node

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
    removed = format_node(
        Node(node.key, node.value.old, REMOVED), depth
    )
    added = format_node(
        Node(node.key, node.value.new, ADDED), depth
    )

    return f'{removed}\n{added}'


def format_node(node, depth=1):
    indent = get_indent(depth)
    sign = get_sign(node.type)
    node_value = node.value

    if isinstance(node.value, dict):
        nodes = []
        for key, value in node.value.items():
            nodes.append(Node(key, value, UNCHANGED))

        node_value = format_nodes(nodes, depth + 1)

    return f'{indent}{sign} {node.key}: {stringify(node_value)}'


def format_nested_node(node, depth=1):
    return format_node(
        Node(node.key, format_nodes(node.value, depth + 1), node.type), depth
    )


def format_nodes(nodes, depth=1):
    result = []
    for node in sorted(nodes):
        if node.type == NESTED:
            result.append(format_nested_node(node, depth))
        elif node.type == UPDATED:
            result.append(format_updated_node(node, depth))
        else:
            result.append(format_node(node, depth))

    indent = ' ' * (INDENT * (depth - 1))
    return '{\n' + '\n'.join(result) + f'\n{indent}}}'


def format_stylish(diff):
    return format_nodes(diff)
