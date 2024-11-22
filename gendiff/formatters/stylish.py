from gendiff.config import INDENT


def render_stylish(data, result=None, depth=1, diff_symbol=' '):
    result = result or []

    indent = ' ' * (INDENT * depth - 2)
    for k, v in data.items():
        if isinstance(v, dict):
            result.append(f'{indent}{diff_symbol} {k}: {{')
            render_stylish(v, result, depth + 1, ' ')
            result.append(f'{indent}  }}')
        else:
            if isinstance(v, bool):
                v = str(v).lower()
            elif v is None:
                v = 'null'
            result.append(f'{indent}{diff_symbol} {k}: {v}')

    return result


def format_stylish(diff):
    def format(data, result, depth=1):
        indent = ' ' * (INDENT * depth - 2)

        for k, v in sorted(data.items()):
            if 'children' in v:
                result.append(f'{indent}  {k}: {{')
                format(v['children'], result, depth + 1)
                result.append(f'{indent}  }}')
            elif 'state' in v:
                diff_symbol = '-' if v['state'] == 'removed' or v['state'] == 'updated' else '+'
                result.extend(render_stylish({k: v['value']}, depth=depth, diff_symbol=diff_symbol))

                if v['state'] == 'updated':
                    result.extend(render_stylish({k: v['new_value']}, depth=depth, diff_symbol='+'))
            else:
                result.extend(render_stylish({k: v}, depth=depth, diff_symbol=' '))

        return result

    result = ['{']
    result = format(diff, result)
    result.append('}')

    return result
