from gendiff.config import INDENT


def stringify(data, result=None, depth=1, diff_symbol=' '):
    result = result or []

    indent = ' ' * (INDENT * depth - 2)
    for key, node in data.items():
        if isinstance(node, dict):
            result.append(f'{indent}{diff_symbol} {key}: {{')
            stringify(node, result, depth + 1, ' ')
            result.append(f'{indent}  }}')
        else:
            if isinstance(node, bool):
                node = str(node).lower()
            elif node is None:
                node = 'null'
            result.append(f'{indent}{diff_symbol} {key}: {node}')

    return result


def format_stylish(diff):
    def format(data, result, depth=1):
        indent = ' ' * (INDENT * depth - 2)

        for k, node in sorted(data.items()):
            if 'children' in node:
                result.append(f'{indent}  {k}: {{')
                format(node['children'], result, depth + 1)
                result.append(f'{indent}  }}')
            elif 'state' in node:
                diff_symbol = '-' if node['state'] == 'removed' or node['state'] == 'updated' else '+'
                result.extend(stringify({k: node['value']}, depth=depth, diff_symbol=diff_symbol))

                if node['state'] == 'updated':
                    result.extend(stringify({k: node['new_value']}, depth=depth, diff_symbol='+'))
            else:
                result.extend(stringify({k: node}, depth=depth))

        return result

    result = ['{']
    result = format(diff, result)
    result.append('}')

    return '\n'.join(result)
