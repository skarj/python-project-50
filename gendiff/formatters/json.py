import json


def convert_nodes_to_dict(nodes):
    result = {}

    for node in nodes:
        value = node.value
        key = node.key

        if isinstance(value, list):
            value = convert_nodes_to_dict(value)

        result[key] = {'value': value, 'type': node.type}

    return result


def format_json(data):
    result = convert_nodes_to_dict(data)

    return json.dumps(result)
