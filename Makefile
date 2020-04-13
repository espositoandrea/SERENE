.PHONY: thesis docs

thesis:
	cd thesis && $(MAKE) dist

docs:
	cd docs/src && $(MAKE)
