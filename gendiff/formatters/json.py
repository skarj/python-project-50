import json
from gendiff.states import ADDED, UPDATED, REMOVED

INDENT = 4


def format_json(data):
    return json.dumps(data, indent=INDENT, sort_keys=True)
