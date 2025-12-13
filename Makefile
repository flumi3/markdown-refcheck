ROOT_DIR := $(CURDIR)
REFCHECK := $(ROOT_DIR)/refcheck

# Detect operating system and shell
ifeq ($(OS),Windows_NT)
    # Windows fallback: no color in CMD, but modern terminals support ANSI
    COLOR_RESET=[0m
    COLOR_BLUE_BG=[44m
    COLOR_GREEN=[32m
    COLOR_RED=[31m
    COLOR_YELLOW=[33m
    COLOR_CYAN=[36m
    COLOR_BOLD=[1m
else
    COLOR_RESET=\033[0m
    COLOR_BLUE_BG=\033[44m
    COLOR_GREEN=\033[32m
    COLOR_RED=\033[31m
    COLOR_YELLOW=\033[33m
    COLOR_CYAN=\033[36m
    COLOR_BOLD=\033[1m
endif

SEPARATOR_LINE=─────────────────────────────────────────────────────────────────
PRINT_SEPARATOR=@echo "$(COLOR_RESET)$(SEPARATOR_LINE)" 

# Print help message if a user only types 'make' without arguments
.DEFAULT_GOAL := help


# --- General commands ---

.PHONY: help
help: ## Display this help message
	@$(PRINT_SEPARATOR)
	@echo "$(COLOR_BOLD)$(COLOR_CYAN)Available commands:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@$(PRINT_SEPARATOR)

.PHONY: init
init: ## Initialize the development environment for all modules
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Initializing Core Environment $(COLOR_RESET)"
	@poetry install
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Installing pre-commit hooks $(COLOR_RESET)"
	@poetry run pre-commit install --hook-type commit-msg --hook-type pre-push
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

# --- Quality Assurance ---

.PHONY: format
format: ## Format code with Ruff 	
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Formatting code with Ruff $(COLOR_RESET)"
	@poetry run ruff format
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: format-check
format-check: ## Check code formatting without modifying files
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Checking code formatting with Ruff $(COLOR_RESET)"
	@poetry run ruff format --check
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: lint
lint: ## Lint code with Ruff
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Linting code with Ruff $(COLOR_RESET)"
	@poetry run ruff check --fix
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: lint-check
lint-check: ## Check linting without modifying files
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Checking linting with Ruff $(COLOR_RESET)"
	@poetry run ruff check
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: check-types
check-types: ## Check typing with MyPy
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Checking typing with MyPy $(COLOR_RESET)"
	@poetry run mypy refcheck
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: check-dead-code
check-dead-code: ## Check for dead code with Vulture
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Checking for dead code with Vulture $(COLOR_RESET)"
	@poetry run vulture refcheck
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: check-unused-deps
check-unused-deps: ## Check for unused dependencies with Deptry
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Checking for unused dependencies with Deptry $(COLOR_RESET)"
	@poetry run deptry .
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: qa
qa: format lint check-types check-dead-code check-unused-deps ## Run all quality assurance checks

.PHONY: ci-qa
ci-qa: format-check lint-check check-types check-dead-code check-unused-deps ## Run all quality assurance checks for CI (non-modifying)

# --- Tests ---

.PHONY: test
test: ## Run tests with pytest
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Running tests with Pytest $(COLOR_RESET)"
	@poetry run pytest
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Running tests with coverage$(COLOR_RESET)"
	@poetry run pytest --cov=refcheck --cov-report=term-missing
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

# --- Version Management ---

.PHONY: bump-version
bump-version: ## Preview what the next version would be
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Previewing version bump $(COLOR_RESET)"
	@poetry run cz bump --dry-run
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: changelog
changelog: ## Show unreleased changelog entries
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Generating changelog preview $(COLOR_RESET)"
	@poetry run cz changelog --dry-run --unreleased-version "Unreleased"
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: check-version
check-version: ## Display current and next version
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Version Information $(COLOR_RESET)"
	@echo "Current version: $$(grep 'version = "' pyproject.toml | head -1 | sed 's/.*version = \"\(.*\)\"/\1/')"
	@echo "Next version (preview):"
	@poetry run cz bump --dry-run 2>&1 | grep -E "(bump|tag to create)" || echo "  No version bump detected"
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"

.PHONY: update-hooks
update-hooks: ## Update pre-commit hooks to latest versions
	@echo "$(COLOR_BLUE_BG)$(COLOR_BOLD) ➜ Updating pre-commit hooks $(COLOR_RESET)"
	@poetry run pre-commit autoupdate
	@echo "$(COLOR_GREEN) ✔ Done$(COLOR_RESET)"
