.PHONY: build-package
build-package:
	- pip install -e .

.PHONY: linting
linting:
	- flake8 src/pyfidelius

.PHONY: run-tests
run-tests:
	- pytest

.PHONY: upload-package
upload-package:
	- python3 -m pip install --upgrade build 
	- python3 -m build
	- py -m pip install --upgrade build
	- py -m build
	- python3 -m pip install --upgrade twine
	- py -m pip install --upgrade twine
	- twine upload dist/*