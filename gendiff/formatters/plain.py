def format_plain(data):
    result = []
    for k, v in sorted(data.items()):

        value = v['value']
        state = v['state']
        if 'new_value' in v:
            new_value = v['new_value']

            if isinstance(new_value, bool):
                new_value = str(new_value).lower()

        if isinstance(value, bool):
            value = str(value).lower()

        if value is None:
            value = 'null'

        if state == 'removed':
            result.append(f"Property '{k}' was removed")

        if state == 'added':
            result.append(f"Property '{k}' was added with value: {value}")

        if state == 'updated':
            result.append(f"Property '{k}' was updated. From {value} to {new_value}")

    return result
