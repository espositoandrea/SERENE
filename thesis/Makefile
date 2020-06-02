BASEFILENAME = Thesis
SOURCE_DIR = src
OUTPUT_FILENAME = thesis-esposito-`date +%Y%m%d`T`date +%H%M`

all: build

clean:
	cd "$(SOURCE_DIR)" && rm -f *.bcf *.run.xml *.aux *.glo *.idx *.log *.toc *.ist *.acn *.acr *.alg *.bbl *.blg *.dvi *.glg *.gls *.ilg *.ind *.lof *.lot *.maf *.mtc *.mtc1 *.out *.synctex.gz "*.synctex(busy)" *.thm

build:
	cd "$(SOURCE_DIR)" && latexmk --synctex=1 --shell-escape "$(BASEFILENAME).tex" -pdf -jobname="$(OUTPUT_FILENAME)" -silent

dist: | build
	mkdir -p out
	cp "$(SOURCE_DIR)/$(BASEFILENAME).pdf" out/

titles:
	cd "$(SOURCE_DIR)" && python add-titles-labels.py

chapter:
ifndef NUM
	$(error NUM is undefined. Use it as make chapter NUM)
endif
	cd "$(SOURCE_DIR)"/chapters && mkdir "chapter$(NUM)"
	cd "$(SOURCE_DIR)"/chapters/chapter$(NUM) && .mkdir images
	cd "$(SOURCE_DIR)"/chapters/chapter$(NUM) && mkdir tables
	@echo % Author: Andrea Esposito > "$(SOURCE_DIR)"/chapters/chapter$(NUM)/chapter$(NUM).tex
