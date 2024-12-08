import json

import yaml


def parse_file(text, extention):
    if extention not in {'.json', '.yaml', '.yml'}:
        raise ValueError(f'Unsupported format type: {extention}')
    elif extention in {'.yaml', '.yml'}:
        return yaml.safe_load(text)
    else:
        return json.loads(text)
