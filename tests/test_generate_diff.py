import pytest
from gendiff.generate_diff import generate_diff


@pytest.fixture(name='input_files')
def _input_files():
    return {
        'json1': 'tests/fixtures/file1.json',
        'json2': 'tests/fixtures/file2.json',
        'yaml1': 'tests/fixtures/file1.yaml',
        'yaml2': 'tests/fixtures/file2.yaml',
    }


@pytest.fixture(name='result1')
def _result1():
    with open('tests/fixtures/result1') as result:
        return result.read().strip()


def test_compare_correct_json_files(input_files, result1):
    assert generate_diff(input_files['json1'], input_files['json2']) == result1


def test_compare_correct_yaml_files(input_files, result1):
    assert generate_diff(input_files['yaml1'], input_files['yaml2']) == result1


def test_compare_correct_yam_json_files(input_files, result1):
    assert generate_diff(input_files['yaml1'], input_files['json2']) == result1


def test_unsupported_file_format(input_files, result1):
    assert generate_diff(input_files['yaml1'], 'tests/fixtures/file2.xml') == 'Error! Unsupported format type: .xml'
