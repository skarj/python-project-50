def stringify(value):
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
    def walk(data, result=[], current_path=''):
        for key, node in sorted(data.items()):
            path = f"{current_path}.{key}" if current_path else key

            if 'children' in node:
                walk(node['children'], result, path)
            elif 'state' in node:
                value = stringify(node['value'])
                new_value = stringify(node.get('new_value'))

                state = node['state']
                if state == 'removed':
                    result.append(f"Property '{path}' was removed")
                elif state == 'added':
                    result.append(f"Property '{path}' was added with value: {value}")
                elif state == 'updated':
                    result.append(f"Property '{path}' was updated. From {value} to {new_value}")

        return result

    return '\n'.join(walk(data))
