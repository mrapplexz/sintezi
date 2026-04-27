MODULE ?= test/sintezi_test

.PHONY: test lint

test:
	@echo "Running tests for $(MODULE)..."
	@uv run python -m pytest $(MODULE)

lint:
	@echo "Formatting"
	@uv run ruff format
	@echo "Auto-Fixing Imports"
	@uv run ruff check --fix
	@echo "Running linting"
	@uv run ruff check
	@echo "Running type checking"
	@uv run ty check
