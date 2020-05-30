init:
	python3 -m pip install pipenv
	pipenv sync --dev

lint:
	pipenv run pylint --rcfile=.pylintrc analyzer -f colorized --exit-zero

build:
	pipenv run python ./setup.py sdist bdist_wheel

test: | lint
	# py.test tests

.PHONY: init test lint build
