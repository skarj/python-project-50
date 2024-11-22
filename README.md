[![Maintainability](https://api.codeclimate.com/v1/badges/e3ca9c69384cf7c1a059/maintainability)](https://codeclimate.com/github/skarj/python-project-50/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e3ca9c69384cf7c1a059/test_coverage)](https://codeclimate.com/github/skarj/python-project-50/test_coverage)
[![Actions Status](https://github.com/skarj/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/skarj/python-project-50/actions)

# Gendiff
Compare two configuration files and show a difference

## Flat Diff for JSON files
TODO: add demo

## Flat Diff for YAML files
TODO: add demo

## Requirements

Python 3.10+

## Installation

```bash
git clone https://github.com/skarj/python-project-50.git
cd python-project-50
make install # Install dependencies
make build # Buld package
make package-install # Install package locally
```

## Running
```bash
$ poetry run gendiff -h

usage: gendiff [-h] [-f {stylish,plain,json}] first_file second_file

Compares two configuration files and shows a difference

positional arguments:
  first_file
  second_file

options:
  -h, --help            show this help message and exit
  -f {stylish,plain,json}, --format {stylish,plain,json}
                        set format of output (default: stylish)
```
