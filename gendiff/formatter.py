def render_stylish(json, depth=1, diff_symbol=' ',
                indent_symbol=' ', indent_size=4):

    def parse(data, result, depth, diff_symbol):
        indent = indent_symbol * (indent_size * depth - 2)
        for k, v in data.items():
            if isinstance(v, dict):
                result.append(f'{indent}{diff_symbol} {k}: {{')
                parse(v, result, depth + 1, ' ')
                result.append(f'{indent}  }}')
            else:
                if isinstance(v, bool):
                    v = str(v).lower()
                if v is None:
                    v = 'null'
                result.append(f'{indent}{diff_symbol} {k}: {v}'.rstrip())
        return result

    result = []
    result = parse(json, result, depth, diff_symbol)

    return result


def format_stylish(diff, indent_size=4):

    def format(data, result, depth=1):
        indent = ' ' * (indent_size * depth - 2)

        for k, v in sorted(data.items()):
            if 'children' in v:
                result.append(f'{indent}  {k}: {{')
                format(v['children'], result, depth + 1)
                result.append(f'{indent}  }}')
            else:
                diff_symbol = ' ' if v['state'] == 'unchanged' \
                    else '-' if v['state'] == 'removed' \
                    or v['state'] == 'changed' else '+'
                result.extend(render_stylish({k: v['value']}, depth, diff_symbol))

                if v['state'] == 'changed':
                    result.extend(render_stylish({k: v['new_value']}, depth, '+'))

        return result

    result = ['{']
    result = format(diff, result)
    result.append('}')

    return result
