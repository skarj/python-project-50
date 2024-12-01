from gendiff.states import ADDED, REMOVED, UPDATED, UNCHANGED

INDENT = 4


def stringify(data, result=None, depth=1, diff_symbol=' '):
    if result is None:
        result = []
    indent = ' ' * (INDENT * depth - 2)

    for key, node in data.items():
        if isinstance(node, dict):
            result.append(f'{indent}{diff_symbol} {key}: {{')
            stringify(node, result, depth + 1, ' ')
            result.append(f'{indent}  }}')
        elif isinstance(node, bool):
            result.append(f'{indent}{diff_symbol} {key}: {str(node).lower()}')
        elif node is None:
            result.append(f'{indent}{diff_symbol} {key}: null')
        else:
            result.append(f'{indent}{diff_symbol} {key}: {node}')

    return result


def stringify2(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return value


def format_stylish(diff):
    def inner(data, depth=1, diff_symbol=' '):
        indent = ' ' * (INDENT * depth - 2)

        for key, node in sorted(data.items()):
            if isinstance(node, dict):
                if 'state' in node:
                    value = node['value']
                    if node['state'] == REMOVED:
                        diff_symbol = '-'
                    elif node['state'] == UPDATED:
                        diff_symbol = '-'
                        new_value = value[1]
                        value = value[0]
                    elif node['state'] == ADDED:
                        diff_symbol = '+'
                    elif node['state'] == UNCHANGED:
                        diff_symbol = ' '

                    result.extend(stringify({key: value}, depth=depth, diff_symbol=diff_symbol))
                    if node['state'] == UPDATED:
                        result.extend(stringify({key: new_value}, depth=depth, diff_symbol='+'))
                else:
                    result.append(f'{indent}  {key}: {{')
                    inner(node, depth=depth + 1)
                    result.append(f'{indent}  }}')
            else:
                result.append(f'{indent}{diff_symbol} {key}: {stringify2(node)}')

        return result

    result = ['{']
    result = inner(diff)
    result.append('}')

    return '\n'.join(result)
