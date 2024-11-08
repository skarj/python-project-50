from gendiff.generate_diff import generate_diff


def test_compare_json_objects():
    file1 = 'tests/fixtures/file1.json'
    file2 = 'tests/fixtures/file2.json'

    with open('tests/fixtures/result1') as result:
        assert generate_diff(file1, file2) == result.read().strip()


def test_compare_yaml_objects():
    file1 = 'tests/fixtures/file1.yaml'
    file2 = 'tests/fixtures/file2.yaml'

    with open('tests/fixtures/result1') as result:
        assert generate_diff(file1, file2) == result.read().strip()
