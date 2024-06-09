.PHONY: build-package
build-package:
	- pip install -e .

.PHONY: linting
linting:
	- flake8 src/pyfidelius

.PHONY: run-tests
run-tests:
	- pytest