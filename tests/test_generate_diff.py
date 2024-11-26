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
        'yaml1': 'tests/fixtures/complex1.yaml',
        'yaml2': 'tests/fixtures/complex2.yaml',
    }


@pytest.fixture(name='result_stylish_simple')
def _result_stylish_simple():
    with open('tests/fixtures/simple_stylish_result') as result:
        return result.read().strip()


@pytest.fixture(name='result_plain_simple')
def _result_plain_simple():
    with open('tests/fixtures/simple_plain_result') as result:
        return result.read().strip()


@pytest.fixture(name='result_json_simple')
def _result_json_simple():
    with open('tests/fixtures/simple_json_result') as result:
        return result.read().strip()


@pytest.fixture(name='result_stylish_complex')
def _result_stylish_complex():
    with open('tests/fixtures/complex_stylish_result') as result:
        return result.read().strip()


@pytest.fixture(name='result_plain_complex')
def _result_plain_complex():
    with open('tests/fixtures/complex_plain_result') as result:
        return result.read().strip()


@pytest.fixture(name='result_json_complex')
def _result_json_complex():
    with open('tests/fixtures/complex_json_result') as result:
        return result.read().strip()


def test_simple_json_plain(input_files_simple, result_plain_simple):
    assert generate_diff(
        input_files_simple['json1'],
        input_files_simple['json2'],
        format_name='plain'
    ) == result_plain_simple


def test_simple_json_stylish(input_files_simple, result_stylish_simple):
    assert generate_diff(
        input_files_simple['json1'],
        input_files_simple['json2']
    ) == result_stylish_simple


def test_simple_yaml_stylish(input_files_simple, result_stylish_simple):
    assert generate_diff(
        input_files_simple['yaml1'],
        input_files_simple['yaml2']
    ) == result_stylish_simple


def test_simple_json_json(input_files_simple, result_json_simple):
    assert generate_diff(
        input_files_simple['json1'],
        input_files_simple['json2'],
        format_name='json'
    ) == result_json_simple


def test_complex_json_stylish(input_files_complex, result_stylish_complex):
    assert generate_diff(
        input_files_complex['json1'],
        input_files_complex['json2']
    ) == result_stylish_complex


def test_complex_json_plain(input_files_complex, result_plain_complex):
    assert generate_diff(
        input_files_complex['json1'],
        input_files_complex['json2'],
        format_name='plain'
    ) == result_plain_complex


def test_complex_yaml_stylish(input_files_complex, result_stylish_complex):
    assert generate_diff(
        input_files_complex['yaml1'],
        input_files_complex['yaml2']
    ) == result_stylish_complex


def test_complex_json_json(input_files_complex, result_json_complex):
    assert generate_diff(
        input_files_complex['json1'],
        input_files_complex['json2'],
        format_name='json'
    ) == result_json_complex


def test_complex_json_yaml_stylish(input_files_complex, result_stylish_complex):
    assert generate_diff(
        input_files_complex['yaml1'],
        input_files_complex['json2']
    ) == result_stylish_complex


# def test_unsupported_file_format(input_files_simple):
#     assert generate_diff(
#         input_files_simple['yaml1'],
#         'tests/fixtures/file2.xml'
#     ) == 'Error! Unsupported format type: .xml'
