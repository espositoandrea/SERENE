# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

all:
	cd ../../emotions/ && doxygen Doxyfile
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)"
	mv "$(BUILDDIR)/**" ..
	rm "$(BUILDDIR)"
