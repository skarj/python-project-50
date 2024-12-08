from gendiff.formatters.json import format_json
from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish

FORMATTERS = {
    'stylish': format_stylish,
    'plain': format_plain,
    'json': format_json
}


def get_formatter(format_name):
    return FORMATTERS[format_name]
