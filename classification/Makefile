zip:
	rm -f classification.zip
	zip -r classification.zip ./classification/ ./setup.py ./requirements.txt ./sample.py -x ./**/__pycache__/\*

lint:
	pylint --rcfile=.pylintrc classification -f colorized --exit-zero

build:
	python3 ./setup.py sdist bdist_wheel

test: | lint
	# py.test tests

.PHONY: test lint build