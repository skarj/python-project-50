import json

import yaml


def parse_file(text, extention):
    if extention in {'.yaml', '.yml'}:
        return yaml.safe_load(text)
    else:
        return json.loads(text)
