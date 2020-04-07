@echo off

SET BASEFILENAME=Thesis
SET SOURCE_DIR=src

IF /I "%1"=="all" GOTO all
IF /I "%1"=="clean" GOTO clean
IF /I "%1"=="build" GOTO build
IF /I "%1"=="dist" GOTO dist
IF /I "%1"=="titles" GOTO titles
IF /I "%1"=="chapter" GOTO chapter
IF /I "%1"=="	@echo % Author" GOTO 	@echo % Author
IF /I "%1"=="" GOTO all
GOTO error

:all
	CALL make.bat build
	GOTO :EOF

:clean
	PUSHD "%SOURCE_DIR%" && DEL /Q *.bcf *.run.xml *.aux *.glo *.idx *.log *.toc *.ist *.acn *.acr *.alg *.bbl *.blg *.dvi *.glg *.gls *.ilg *.ind *.lof *.lot *.maf *.mtc *.mtc1 *.out *.synctex.gz "*.synctex(busy)" *.thm /F && POPD
	GOTO :EOF

:build
	@echo "\033[32mCompiling LaTeX (1/4):\033[0m"
	PUSHD "%SOURCE_DIR%" && pdflatex -synctex=1 -interaction=batchmode --shell-escape "%BASEFILENAME%.tex" && POPD
	@echo "\033[32mBuilding bibliography (2/4):\033[0m"
	PUSHD "%SOURCE_DIR%" && biber "%BASEFILENAME%" && POPD
	@echo "\033[32mCompiling LaTeX (3/4):\033[0m"
	PUSHD "%SOURCE_DIR%" && pdflatex -synctex=1 -interaction=batchmode --shell-escape "%BASEFILENAME%.tex" && POPD
	@echo "\033[32mCompiling LaTeX (4/4):\033[0m"
	PUSHD "%SOURCE_DIR%" && pdflatex -synctex=1 -interaction=batchmode --shell-escape "%BASEFILENAME%.tex" && POPD
	GOTO :EOF

:dist
	CALL make.bat build
	MKDIR out
	XCOPY /Y "%SOURCE_DIR%/%BASEFILENAME%.pdf" out/ 
	GOTO :EOF

:titles
	PUSHD "%SOURCE_DIR%" && python add-titles-labels.py && POPD
	GOTO :EOF

:chapter
	GOTO :EOF

:	@echo % Author
	CALL make.bat Andrea
	CALL make.bat Esposito
	CALL make.bat >
	CALL make.bat "$(SOURCE_DIR)"/chapters/chapter$(NUM)/chapter$(NUM).tex
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
