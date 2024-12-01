from gendiff.states import ADDED, UPDATED, REMOVED


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
    def inner(data, current_path=''):
        for key, node in sorted(data.items()):
            path = f"{current_path}.{key}" if current_path else key

            if 'state' in node:
                state = node['state']
                if state == REMOVED:
                    result.append(f"Property '{path}' was removed")
                elif state == ADDED:
                    value = stringify(node['value'])
                    result.append(f"Property '{path}' was added with value: {value}")
                elif state == UPDATED:
                    value = stringify(node['value'][0])
                    new_value = stringify(node['value'][1])
                    result.append(f"Property '{path}' was updated. "
                                  f"From {value} to {new_value}")
            else:
                inner(node, path)

        return result

    result = []
    result = inner(data)

    return '\n'.join(result)
