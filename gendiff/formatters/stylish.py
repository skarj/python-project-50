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


def format_stylish(diff):
    def inner(data, depth=1):
        indent = ' ' * (INDENT * depth - 2)

        for key, node in sorted(data.items()):
            if 'state' in node:
                value = node['value']
                if node['state'] == REMOVED:
                    result.extend(stringify({key: value}, depth=depth, diff_symbol='-'))
                elif node['state'] == UPDATED:
                    result.extend(stringify({key: value[0]}, depth=depth, diff_symbol='-'))
                    result.extend(stringify({key: value[1]}, depth=depth, diff_symbol='+'))
                elif node['state'] == ADDED:
                    result.extend(stringify({key: value}, depth=depth, diff_symbol='+'))
                elif node['state'] == UNCHANGED:
                    result.extend(stringify({key: value}, depth=depth))
            else:
                result.append(f'{indent}  {key}: {{')
                inner(node, depth=depth + 1)
                result.append(f'{indent}  }}')

        return result

    result = ['{']
    result = inner(diff)
    result.append('}')

    return '\n'.join(result)
