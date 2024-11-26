import json
from gendiff.config import INDENT


def format_json(data):
    def format(data, result=[], current_path=''):
        for key, node in sorted(data.items()):
            path = f"{current_path}.{key}" if current_path else key

            if 'children' in node:
                format(node['children'], result, path)
            elif 'state' in node:
                value = node['value']
                new_value = node.get('new_value')

                state = node['state']
                if state == 'removed':
                    result.append({
                        "path": path,
                        "state": state
                    })
                elif state == 'added':
                    result.append({
                        "path": path,
                        "state": state,
                        "value": value
                    })
                elif state == 'updated':
                    result.append({
                        "path": path,
                        "state": state,
                        "value": value,
                        "new_value": new_value
                    })

        return result

    return json.dumps(format(data), indent=INDENT)
