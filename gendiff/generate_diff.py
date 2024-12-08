from gendiff.diff import create_diff
from gendiff.file import get_extention, load_file
from gendiff.formatters.utils import get_formatter
from gendiff.parse import parse_file


def generate_diff(file_path1, file_path2, format_name='stylish'):
    file1_extention = get_extention(file_path1)
    file2_extention = get_extention(file_path2)

    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    content1 = parse_file(file1, file1_extention)
    content2 = parse_file(file2, file2_extention)

    diff = create_diff(content1, content2)
    formatter = get_formatter(format_name)

    return formatter(diff)
