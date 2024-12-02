from gendiff.types import ADDED, REMOVED, UPDATED, UNCHANGED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def get_sign(type):
    if type == ADDED:
        return '+'
    elif type == REMOVED:
        return '-'
    elif type == UNCHANGED:
        return ' '


def get_indent(depth=1):
    return ' ' * (INDENT * depth - 2)


def format_updated_node(node):
    key, prop = node
    value = prop['value']
    value_old, value_new = value

    removed = format_node((key, {"value": value_old, "type": REMOVED}))
    added = format_node((key, {"value": value_new, "type": ADDED}))

    return f'{removed}\n{added}'


def format_node(node):
    indent = get_indent()

    key, prop = node
    type = prop['type']
    value = prop['value']
    sign = get_sign(type)

    return f'{indent}{sign} {key}: {stringify(value)}'


def format_stylish(diff):
    result = []
    for node in sorted(diff.items()):
        _, prop = node
        type = prop['type']

        if type == UPDATED:
            result.append(format_updated_node(node))
        else:
            result.append(format_node(node))

    return "{\n" + '\n'.join(result) + "\n}"
