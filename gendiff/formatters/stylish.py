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


def format_updated(node):
    indent = get_indent()

    key, prop = node
    value = prop['value']
    value_old, value_new = value
    sign_added = get_sign(ADDED)
    sign_removed = get_sign(REMOVED)

    return f'{indent}{sign_removed} {key}: {stringify(value_old)}\n' + \
           f'{indent}{sign_added} {key}: {stringify(value_new)}'


def format_node(node):
    key, prop = node
    type = prop['type']

    if type == UPDATED:
        return format_updated(node)

    indent = get_indent()
    sign = get_sign(type)

    value = prop['value']
    return f'{indent}{sign} {key}: {stringify(value)}'


def format_stylish(diff):
    result = []
    for node in sorted(diff.items()):
        result.append(format_node(node))

    return "{\n" + '\n'.join(result) + "\n}"
