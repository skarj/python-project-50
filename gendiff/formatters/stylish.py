from gendiff.types import ADDED, REMOVED, UPDATED, UNCHANGED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def get_sign(node):
    _, prop = node
    if prop['type'] == ADDED:
        return '+'
    elif prop['type'] == REMOVED:
        return '-'
    elif prop['type'] == UPDATED:
        return ('-', '+')
    elif prop['type'] == UNCHANGED:
        return ' '


def format_simple(node, depth=1):
    indent = ' ' * (INDENT * depth - 2)
    sign = get_sign(node)

    key, prop = node
    value = prop['value']

    if prop['type'] == UPDATED:
        sign_del, sign_add = sign
        sign = sign_del
        value_old, value_new = value
        value = value_old

    result = f'{indent}{sign} {key}: {stringify(value)}'

    if prop['type'] == UPDATED:
        result = result + f'\n{indent}{sign_add} {key}: {stringify(value_new)}'

    return result


def format_stylish(diff):
    result = []
    for node in sorted(diff.items()):
        result.append(format_simple(node))

    return "{\n" + '\n'.join(result) + "\n}"
