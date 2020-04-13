PUSHD ..\..\emotions\ && doxygen Doxyfile && POPD
sphinx-build -b html .\ .\_build
XCOPY /S /Q /Y .\_build\** ..\
RMDIR /S /Q .\_build
