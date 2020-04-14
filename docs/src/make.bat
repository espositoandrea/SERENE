@echo off

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
SET SOURCEDIR=.
SET BUILDDIR=_build

IF /I "%1"=="all" GOTO all
IF /I "%1"=="" GOTO all
GOTO error

:all
	PUSHD ..\..\emotions\ && doxygen Doxyfile && POPD
	%SPHINXBUILD% -b html "%SOURCEDIR%" "%BUILDDIR%"
	XCOPY /S /Q /Y "%BUILDDIR%\**" ..
	RMDIR /S /Q "%BUILDDIR%" 
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
