from gendiff.generate_diff import ADDED, NESTED, REMOVED, UPDATED


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


def format_plain(diff):
    result = []

    def inner(diff, current_path=''):
        for node in sorted(diff):
            key = node.key
            path = f"{current_path}.{key}" if current_path else key

            type = node.type
            if type == REMOVED:
                result.append(f"Property '{path}' was removed")

            elif type == ADDED:
                value = stringify(node.value)
                result.append(f"Property '{path}' was added "
                              f'with value: {value}')
            elif type == UPDATED:
                value = stringify(node.value.old)
                new_value = stringify(node.value.new)
                result.append(f"Property '{path}' was updated. "
                              f'From {value} to {new_value}')
            elif type == NESTED:
                inner(node.value, path)

        return result

    inner(diff)

    return '\n'.join(result)
