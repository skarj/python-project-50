from gendiff.states import ADDED, REMOVED, UPDATED, UNCHANGED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return value


def format_stylish(diff):
    def inner(data, depth=1):
        indent = ' ' * (INDENT * depth - 2)
        result = []

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

                    if isinstance(value, dict):
                        result.append(f'{indent}{diff_symbol} {key}: {{')
                        result.extend(inner(value, depth + 1))
                        result.append(f'{indent}  }}')
                    else:
                        result.append(f'{indent}{diff_symbol} {key}: {stringify(value)}')
                    if node['state'] == UPDATED:
                        result.append(f'{indent}+ {key}: {stringify(new_value)}')
                else:
                    result.append(f'{indent}  {key}: {{')
                    result.extend(inner(node, depth + 1))
                    result.append(f'{indent}  }}')
            else:
                result.append(f'{indent}  {key}: {stringify(node)}')

        return result

    result = ['{']
    result.extend(inner(diff))
    result.append('}')

    return '\n'.join(result)
