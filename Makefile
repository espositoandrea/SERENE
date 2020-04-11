.PHONY: thesis

thesis:
	cd thesis && $(MAKE) dist

cppdoc:
	cd emotions && doxygen Doxyfile
