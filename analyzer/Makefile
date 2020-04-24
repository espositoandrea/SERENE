init:
	python3 -m pip install -r requirements.txt

lint:
	pylint --rcfile=.pylintrc analyzer -f colorized --exit-zero

test: | lint
	# py.test tests

.PHONY: init test lint
