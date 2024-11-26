import json
from gendiff.states import ADDED, UPDATED, REMOVED

INDENT = 4


def format_json(data):
    def format(data, result=None, current_path=''):
        if result is None:
            result = []

        for key, node in sorted(data.items()):
            path = f"{current_path}.{key}" if current_path else key

            if 'children' in node:
                format(node['children'], result, path)
            elif 'state' in node:
                value = node['value']
                new_value = node.get('new_value')

                state = node['state']
                if state == REMOVED:
                    result.append({
                        "path": path,
                        "state": state
                    })
                elif state == ADDED:
                    result.append({
                        "path": path,
                        "state": state,
                        "value": value
                    })
                elif state == UPDATED:
                    result.append({
                        "path": path,
                        "state": state,
                        "value": value,
                        "new_value": new_value
                    })

        return result

    return json.dumps(format(data), indent=INDENT)
