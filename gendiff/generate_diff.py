from collections import namedtuple

REMOVED = 'removed'
ADDED = 'added'
UPDATED = 'updated'
UNCHANGED = 'unchanged'
NESTED = 'nested'

Node = namedtuple('Node', 'key value type')
ChangedValue = namedtuple('ChangedValue', 'old new')


def create_diff(content1, content2):
    diff = []
    for key in content1.keys() - content2.keys():
        value = content1[key]
        diff.append(Node(key, value, REMOVED))

    for key in content2.keys() - content1.keys():
        value = content2[key]
        diff.append(Node(key, value, ADDED))

    for key in content2.keys() & content1.keys():
        old_value = content1[key]
        new_value = content2[key]

        if isinstance(old_value, dict) and isinstance(new_value, dict):
            diff.append(Node(key, create_diff(old_value, new_value), NESTED))
        elif old_value != new_value:
            changed_value = ChangedValue(old_value, new_value)
            diff.append(Node(key, changed_value, UPDATED))
        else:
            diff.append(Node(key, old_value, UNCHANGED))

    return diff
