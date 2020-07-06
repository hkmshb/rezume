.PHONY: lint test

lint:
	tox -e lint

test:
	tox -e test
