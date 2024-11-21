def format_plain(data, result=[]):
    for k, v in sorted(data.items()):
        if 'children' in v:
            format_plain(v['children'])
        else:
            value = v['value']
            state = v['state']
            if 'new_value' in v:
                new_value = v['new_value']

                if isinstance(new_value, bool):
                    new_value = str(new_value).lower()
                elif isinstance(new_value, dict):
                    new_value = '[complex value]'
                elif isinstance(new_value, str):
                    new_value = f"'{new_value}'"
                elif new_value is None:
                    new_value = 'null'

            if isinstance(value, bool):
                value = str(value).lower()
            elif isinstance(value, dict):
                value = '[complex value]'
            elif isinstance(value, str):
                value = f"'{value}'"
            elif value is None:
                value = 'null'

            if state == 'removed':
                result.append(f"Property '{k}' was removed")

            if state == 'added':
                result.append(f"Property '{k}' was added with value: {value}")

            if state == 'updated':
                result.append(f"Property '{k}' was updated. From {value} to {new_value}")

    return result
