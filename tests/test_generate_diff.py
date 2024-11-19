import pytest
from gendiff.generate_diff import generate_diff


@pytest.fixture(name='input_files_simple')
def _input_files_simple():
    return {
        'json1': 'tests/fixtures/simple1.json',
        'json2': 'tests/fixtures/simple2.json',
        'yaml1': 'tests/fixtures/simple1.yaml',
        'yaml2': 'tests/fixtures/simple2.yaml',
    }


@pytest.fixture(name='input_files_complex')
def _input_files_complex():
    return {
        'json1': 'tests/fixtures/complex1.json',
        'json2': 'tests/fixtures/complex2.json',
    }


@pytest.fixture(name='result_simple')
def _result_simple():
    with open('tests/fixtures/simple_result') as result:
        return result.read().strip()


@pytest.fixture(name='result_complex')
def _result_complex():
    with open('tests/fixtures/complex_result') as result:
        return result.read().strip()


def test_compare_correct_json_files(input_files_simple, result_simple):
    assert generate_diff(input_files_simple['json1'], input_files_simple['json2']) == result_simple


def test_compare_correct_json_files_complex(input_files_complex, result_complex):
    assert generate_diff(input_files_complex['json1'], input_files_complex['json2']) == result_complex


def test_compare_correct_yaml_files(input_files_simple, result_simple):
    assert generate_diff(input_files_simple['yaml1'], input_files_simple['yaml2']) == result_simple


def test_compare_correct_yam_json_files(input_files_simple, result_simple):
    assert generate_diff(input_files_simple['yaml1'], input_files_simple['json2']) == result_simple


def test_unsupported_file_format(input_files_simple):
    assert generate_diff(input_files_simple['yaml1'], 'tests/fixtures/file2.xml') == 'Error! Unsupported format type: .xml'
