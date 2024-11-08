import json
from gendiff.generate_diff import compare_objects


def test_compare_objects():
    json1 = json.load(open('tests/fixtures/file1.json'))
    json2 = json.load(open('tests/fixtures/file2.json'))


    with open('tests/fixtures/result1') as result:
        assert compare_objects(json1, json2) == result.read().strip()

