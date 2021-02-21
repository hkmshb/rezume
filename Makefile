TOX := pipx run tox

.PHONY: help clean lint test

# source: https://victoria.dev/blog/django-project-best-practices-to-keep-your-developers-happy/
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all build and temporary artifacts
	rm -rf .tox dist

lint: ## Run linter through project
	$(TOX) -e lint

test: ## Run unit tests for project
	$(TOX) -e test
