.PHONY: extension server logo

all: logo extension server

logo:
	cp logo.svg ../docs/_static/logo.svg

extension:
	inkscape -z icon.svg -e ../extension/src/assets/icon16.png -w 16
	inkscape -z icon.svg -e ../extension/src/assets/icon32.png -w 32
	inkscape -z icon.svg -e ../extension/src/assets/icon48.png -w 48
	inkscape -z icon.svg -e ../extension/src/assets/icon64.png -w 64
	inkscape -z icon.svg -e ../extension/src/assets/icon128.png -w 128

server:
	convert icon.svg -define icon:auto-resize ../server/assets/images/icon.ico
