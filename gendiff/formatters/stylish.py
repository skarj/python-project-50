from gendiff.states import UPDATED, REMOVED

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


def format_stylish(diff):
    def format(data, result, depth=1):
        indent = ' ' * (INDENT * depth - 2)

        for key, node in sorted(data.items()):
            if 'children' in node:
                result.append(f'{indent}  {key}: {{')
                format(node['children'], result, depth + 1)
                result.append(f'{indent}  }}')
            elif 'state' in node:
                diff_symbol = '-' if node['state'] in {REMOVED, UPDATED} else '+'
                result.extend(stringify({key: node['value']}, depth=depth, diff_symbol=diff_symbol))

                if node['state'] == UPDATED:
                    result.extend(stringify({key: node['new_value']}, depth=depth, diff_symbol='+'))
            else:
                result.extend(stringify({key: node}, depth=depth))

        return result

    result = ['{']
    result = format(diff, result)
    result.append('}')

    return '\n'.join(result)
