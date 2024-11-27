from gendiff.states import UPDATED, REMOVED, ADDED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return value


def format_stylish(diff):
    def format(data, result=None, depth=1, diff_symbol=' '):
        if result is None:
            result = []

        indent = ' ' * (INDENT * depth - 2)
        for key, node in sorted(data.items()):
            if isinstance(node, dict):
                if 'children' in node:
                    result.append(f'{indent}  {key}: {{')
                    format(node['children'], result, depth + 1)
                    result.append(f'{indent}  }}')
                elif 'state' in node:
                    state = node.get('state')
                    value = node.get('value')
                    new_value = node.get('new_value')

                    if state == REMOVED:
                        format({key: value}, result, depth, '-')
                    elif state == UPDATED:
                        format({key: value}, result, depth, '-')
                        format({key: new_value}, result, depth, '+')
                    elif state == ADDED:
                        format({key: value}, result, depth, '+')
                    else:
                        format({key: value}, result, depth, ' ')
                else:
                    result.append(f'{indent}{diff_symbol} {key}: {{')
                    format(node, result, depth + 1, diff_symbol=' ')
                    result.append(f'{indent}  }}')
            else:
                result.append(f'{indent}{diff_symbol} {key}: {stringify(node)}')

        return result

    result = ['{']
    result = format(diff, result)
    result.append('}')

    return '\n'.join(result)
