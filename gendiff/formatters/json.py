import json

from gendiff.diff import NESTED, UPDATED


def convert_nodes_to_dict(nodes):
    result = {}

    for node in nodes:
        value = node.value
        key = node.key
        type = node.type

        if type == NESTED:
            value = convert_nodes_to_dict(value)
        elif type == UPDATED:
            value = {"old": value.old, "new": value.new}

        result[key] = {'value': value, 'type': node.type}

    return result


def format_json(data):
    result = convert_nodes_to_dict(data)

    return json.dumps(result)
