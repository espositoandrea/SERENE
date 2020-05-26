init:
    python3 -m pip install pipenv
	pipenv install

lint:
	pipenv run pylint --rcfile=.pylintrc analyzer -f colorized --exit-zero

test: | lint
	# py.test tests

.PHONY: init test lint
