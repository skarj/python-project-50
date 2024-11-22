import json
from gendiff.config import INDENT


def format_json(data):
    def format(data, result=[], current_path=''):
        for k, v in sorted(data.items()):
            path = f"{current_path}.{k}" if current_path else k

            if 'children' in v:
                format(v['children'], result, path)
            elif 'state' in v:
                value = v['value']
                new_value = v.get('new_value')

                state = v['state']
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
