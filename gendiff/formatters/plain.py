def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is None:
        return 'null'
    else:
        return value


def format_plain(data):
    def format(data, result=[], current_path=''):
        for k, v in sorted(data.items()):
            path = f"{current_path}.{k}" if current_path else k

            if 'children' in v:
                format(v['children'], result, path)
            else:
                value = format_value(v['value'])
                new_value = format_value(v.get('new_value'))

                state = v['state']
                if state == 'removed':
                    result.append(f"Property '{path}' was removed")
                elif state == 'added':
                    result.append(f"Property '{path}' was added with value: {value}")
                elif state == 'updated':
                    result.append(f"Property '{path}' was updated. From {value} to {new_value}")

        return result

    return format(data)
