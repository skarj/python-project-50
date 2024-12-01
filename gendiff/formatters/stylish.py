from gendiff.states import ADDED, REMOVED, UPDATED

INDENT = 4


def stringify(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def format_stylish(diff):
    def inner(data, depth=1):
        indent = ' ' * (INDENT * depth - 2)
        result = []

        for key, node in sorted(data.items()):
            if isinstance(node, dict) and 'state' in node:
                value = node['value']
                diff_symbol = {
                    REMOVED: '-', UPDATED: '-', ADDED: '+'
                }.get(node['state'], ' ')

                if node['state'] == UPDATED:
                    new_value = value[1]
                    value = value[0]

                if isinstance(value, dict):
                    result.append(f'{indent}{diff_symbol} {key}: {{')
                    result.extend(inner(value, depth + 1))
                    result.append(f'{indent}  }}')
                else:
                    result.append(f'{indent}{diff_symbol} {key}: {stringify(value)}')

                if node['state'] == UPDATED:
                    if isinstance(new_value, dict):
                        result.append(f'{indent}+ {key}: {{')
                        result.extend(inner(new_value, depth + 1))
                        result.append(f'{indent}  }}')
                    else:
                        result.append(f'{indent}+ {key}: {stringify(new_value)}')
            else:
                if isinstance(node, dict):
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
