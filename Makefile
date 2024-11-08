.PHONY: install test test-coverage lint build package-install selfcheck check gendiff

install:
	poetry install

test:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov gendiff --cov-report=xml

lint:
	poetry run flake8 gendiff

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl --force-reinstall

selfcheck:
	poetry check

check: selfcheck test lint

gendiff:
	poetry run gendiff
