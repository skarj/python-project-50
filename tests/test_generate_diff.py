import pytest
from gendiff.generate_diff import generate_diff


@pytest.fixture(name='input_files')
def _input_files():
    return {
        'json1': 'tests/fixtures/simple1.json',
        'json2': 'tests/fixtures/simple2.json',
        'yaml1': 'tests/fixtures/simple1.yaml',
        'yaml2': 'tests/fixtures/simple2.yaml',
    }


@pytest.fixture(name='simple_result')
def _simple_result():
    with open('tests/fixtures/simple_result') as result:
        return result.read().strip()


def test_compare_correct_json_files(input_files, simple_result):
    assert generate_diff(input_files['json1'], input_files['json2']) == simple_result


def test_compare_correct_yaml_files(input_files, simple_result):
    assert generate_diff(input_files['yaml1'], input_files['yaml2']) == simple_result


def test_compare_correct_yam_json_files(input_files, simple_result):
    assert generate_diff(input_files['yaml1'], input_files['json2']) == simple_result


def test_unsupported_file_format(input_files):
    assert generate_diff(input_files['yaml1'], 'tests/fixtures/file2.xml') == 'Error! Unsupported format type: .xml'
