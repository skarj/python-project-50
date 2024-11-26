from gendiff.formatters.stylish import format_stylish
from gendiff.formatters.plain import format_plain
from gendiff.formatters.json import format_json


def get_formatter(format_name):
    formatters = {
        'stylish': format_stylish,
        'plain': format_plain,
        'json': format_json
    }

    return formatters[format_name]