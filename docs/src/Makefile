all:
	cd ../../emotions/ && doxygen Doxyfile
	sphinx-build -b html . _build
	mv _build/** ..
	rm _build
