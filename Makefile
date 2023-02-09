.PHONY: all
all: clean build test


.PHONY: clean
clean:
	rm -frv dist/ build/ *.egg-info
	rm -frv master/__pycache__
	rm -frv .pytest_cache


.PHONY: build
build: clean
	python3 setup.py sdist bdist_wheel


.PHONY: test
test: build
	# pytest
	pip install -r requirements.txt
	master version
	python3 -m twine upload --repository testpypi dist/*


.PHONY: release
release:
	python3 -m twine upload dist/*
