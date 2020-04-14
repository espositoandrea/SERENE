@echo off


IF /I "%1"=="thesis" GOTO thesis
IF /I "%1"=="docs" GOTO docs
GOTO error

:thesis
	PUSHD thesis && CALL make.bat dist && POPD
	GOTO :EOF

:docs
	PUSHD docs/src && CALL make.bat && POPD
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
