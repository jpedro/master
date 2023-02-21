.PHONY: help
help: ### Shows this help
	@grep -E '^[0-9a-zA-Z_-]+:' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?### "}; {printf "\033[32;1m%-16s\033[0m %s\n", $$1, $$2}'


.PHONY: all
all: clean build test ### Builds and tests


.PHONY: clean
clean: ### Removes temporary files
	rm -frv dist/ build/ *.egg-info
	rm -frv master/__pycache__
	rm -frv .pytest_cache


.PHONY: build
build: clean ### Builds the package locally
	python3 setup.py sdist bdist_wheel


.PHONY: test
test: build ### Tests the package locally
	# pytest
	pip install -r requirements.txt
	master version
	python3 -m twine upload --repository testpypi dist/*


.PHONY: release
release: build ### Deploys the package to pypi
	python3 -m twine upload dist/*
