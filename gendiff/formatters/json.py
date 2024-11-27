import json

INDENT = 4


def format_json(data):
    return json.dumps(data, indent=INDENT, sort_keys=True)
