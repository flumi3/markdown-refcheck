# Contributing to RefCheck

Thank you for your interest in contributing to RefCheck! I welcome contributions and appreciate your help in making this
tool better.

## Table of Contents

- [How Can You Contribute?](#how-can-you-contribute)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Commit Convention](#commit-convention)
- [Development Commands](#development-commands)
- [Testing](#testing)
- [Code Quality Standards](#code-quality-standards)
- [Publishing (Maintainers Only)](#publishing-maintainers-only)
- [Getting Help](#getting-help)

## How Can You Contribute?

### Reporting Bugs

If you find a bug, please create an issue with:

- A clear, descriptive title
- Steps to reproduce the problem
- Expected vs. actual behavior
- Your environment (OS, Python version, RefCheck version)
- Sample Markdown files that demonstrate the issue (if applicable)

### Suggesting Enhancements

Feature requests are welcome too! Please:

- Check existing issues to avoid duplicates
- Clearly describe the feature and its benefits
- Provide examples of how it would be used
- Explain why this would be useful to most users

### Submitting Pull Requests

1. **Fork the repository** and create a branch from `main`
2. **Follow the development setup** instructions below
3. **Make your changes** following the code quality standards
4. **Add tests** for new functionality
5. **Ensure all tests pass** with `make test`
6. **Run quality checks** with `make qa`
7. **Follow commit conventions** (see below)
8. **Submit a pull request** with a clear description of changes

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Initial Setup

1. **Install Poetry** (if not already installed):

   ```bash
   pipx install poetry
   ```

2. **Configure Poetry** to create virtual environments in the project directory:

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. **Clone your fork** of the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/refcheck.git
   cd refcheck
   ```

4. **Initialize the development environment**:

   ```bash
   make init
   ```

   This will:

   - Install all dependencies
   - Set up pre-commit hooks for commit message validation and pre-push checks

5. **Verify the installation** by running RefCheck:

   ```bash
   poetry run refcheck --help
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names that indicate the type of change:

- `feat/add-json-output` - New features
- `fix/handle-empty-files` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/parser-cleanup` - Code refactoring
- `test/add-validator-tests` - Test additions

### Making Changes

1. **Create a new branch** from `main`:

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes** and test them locally:

   ```bash
   poetry run refcheck <test-files>
   ```

   > 💡 **Tip**: Use AI-tools like GitHub copilot, Claude, ChatGPT, etc. to create Markdown test files.

3. **Run quality checks**:

   ```bash
   make qa
   ```

4. **Commit your changes** (see commit convention below)

5. **Push to your fork**:

   ```bash
   git push origin feat/your-feature-name
   ```

6. **Open a pull request** on GitHub

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning and changelog
generation. All commit messages **must** follow this format:

```text
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types That Trigger Version Bumps

- `feat:` - New feature → **minor** version bump (0.1.0 → 0.2.0)
- `fix:` - Bug fix → **patch** version bump (0.1.0 → 0.1.1)
- `perf:` - Performance improvement → **patch** version bump
- `BREAKING CHANGE:` footer or `!` after type → **major** version bump (0.1.0 → 1.0.0)

### Types That Don't Trigger Releases

- `docs:` - Documentation changes only
- `chore:` - Maintenance tasks (dependencies, configs)
- `ci:` - CI/CD pipeline changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code restructuring (no behavior changes)
- `test:` - Adding or updating tests
- `build:` - Build system changes

### Commit Message Examples

**Good commits:**

```bash
feat: add support for checking external URL status codes
fix: handle empty markdown files without crashing
docs: update CLI examples in README
feat!: change CLI argument format to use subcommands
fix(parser): correctly parse markdown links with special characters
perf: optimize reference validation by caching file checks
test: add integration tests for remote URL validation
```

**Bad commits** (will be rejected by pre-commit hooks):

```bash
updated readme
fix bug
WIP
Added new feature
```

### Commit Message Guidelines

- Use imperative mood ("add feature" not "added feature")
- Keep the first line under 72 characters
- Don't end the summary with a period
- Use the body to explain "what" and "why", not "how"
- Reference issues and PRs in the footer: `Fixes #123`, `Closes #456`

## Development Commands

RefCheck uses a Makefile for common development tasks:

```bash
make help              # Show all available commands
make format            # Format code with Ruff
make lint              # Lint and fix code with Ruff
make test              # Run tests with pytest
make test-coverage     # Run tests with coverage report
make qa                # Run all quality checks (format, lint, type check, etc.)
make ci-qa             # Run all quality checks without modifying files (for CI)
make bump-version      # Preview what the next version would be
make changelog         # Show unreleased changelog entries
make check-version     # Display current and next version
make update-hooks      # Update pre-commit hooks to latest versions
```

## Testing

### Running Tests

```bash
# Run all tests with coverage
make test

# Run tests with detailed HTML coverage report
make test-coverage

# Run specific test file
poetry run pytest tests/test_validators/test_file_exists.py

# Run tests matching a pattern
poetry run pytest -k "test_header"
```

### Coverage Requirements

**All pull requests must maintain at least 80% code coverage.** This is enforced by CI/CD pipelines.

- Coverage is measured automatically during test runs
- The build will fail if coverage drops below 80%
- View detailed coverage reports in `htmlcov/index.html` after running `make test-coverage`
- Codecov integration provides coverage diff reports on pull requests

### Writing Tests

- **Add tests for all new functionality** - No new code without tests
- Place tests in the appropriate directory under `tests/`
- Use descriptive test names that explain what is being tested
- **Aim for 90%+ coverage** for new modules (minimum 80% overall)
- Include edge cases and error conditions
- Use fixtures from `tests/conftest.py` for common test setup
- Leverage test fixtures in `tests/fixtures/` for realistic test scenarios

### Test Structure

```python
def test_function_name_with_valid_input():
    """Test that function handles valid input correctly."""
    # Arrange
    input_data = "test input"

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_output
```

## Code Quality Standards

All code must meet these standards before merging:

### Code Formatting

- **Ruff** is used for formatting and linting
- Line length: 100 characters maximum
- Run `make format` before committing

### Type Hints

- Use type hints for all function parameters and return values
- Run `make type-check` to validate types with mypy

### Linting

- Code must pass all Ruff linting rules
- No unused imports or variables (checked by vulture)
- Run `make lint` to check for issues

### Dependencies

- No unnecessary dependencies
- Run `deptry` to check for unused dependencies (included in `make qa`)

### Quality Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`make test`)
- [ ] Code coverage is maintained or improved (`make test-coverage`)
- [ ] All quality checks pass (`make qa`)
- [ ] Commit messages follow conventional commits
- [ ] Documentation is updated if needed

## Publishing (Maintainers Only)

### Automated Publishing

This project uses automated versioning and publishing through GitHub Actions. When commits are pushed to `main`:

1. **Semantic Release** analyzes commit messages
2. **Version is bumped** automatically based on commit types
3. **CHANGELOG.md** is updated
4. **Git tag** is created
5. **Package is built** and published to PyPI

### Manual Publishing (if needed)

1. **Create a PyPI API token** from [PyPI Account Settings](https://pypi.org/manage/account/publishing/)

2. **Configure Poetry** with the token:

   ```bash
   poetry config pypi-token.pypi YOUR_PYPI_API_TOKEN
   ```

3. **Build the package**:

   ```bash
   poetry build
   ```

4. **Publish to PyPI**:

   ```bash
   poetry publish
   ```

## Getting Help

- **Questions?** Open a [GitHub Discussion](https://github.com/flumi3/refcheck/discussions)
- **Bug or Issue?** Create an [Issue](https://github.com/flumi3/refcheck/issues)
- **Want to chat?** Comment on relevant issues or PRs

Thank you for contributing to RefCheck! 🎉
