import os


def load_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def get_extention(file_path):
    _, extention = os.path.splitext(file_path)

    if extention not in {'.json', '.yaml', '.yml'}:
        raise ValueError(f'Unsupported format type: {extention}')

    return extention
