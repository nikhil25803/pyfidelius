.PHONY: build-package
build-package:
	- pip install -e .

.PHONY: linting
linting:
	- flake8 src/pyfidelius

.PHONY: run-tests
run-tests:
	- pytest

.PHONY: build-linux
build-linux:
	- python3 -m pip install --upgrade build 
	- python3 -m build
	- python3 -m pip install --upgrade twine
	- twine upload dist/*

.PHONY: build-windows
build-windows:
	- py -m pip install --upgrade build
	- py -m build
	- py -m pip install --upgrade twine
	- twine upload dist/*