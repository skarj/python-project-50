import json


def format_nodes(nodes):
    result = {}

    for node in nodes:
        value = node.value
        key = node.key

        if isinstance(value, list):
            value = format_nodes(value)

        result[key] = {'value': value, 'type': node.type}

    return result


def format_json(data):
    result = format_nodes(data)

    return json.dumps(result)
