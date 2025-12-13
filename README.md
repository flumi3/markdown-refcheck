# RefCheck

RefCheck is a simple tool for finding broken references and links in Markdown files.

```text
usage: refcheck [OPTIONS] [PATH ...]

positional arguments:
  PATH                  Markdown files or directories to check

options:
  -h, --help            show this help message and exit
  -e, --exclude [ ...]  Files or directories to exclude
  -cm, --check-remote   Check remote references (HTTP/HTTPS links)
  -nc, --no-color        Turn off colored output
  -v, --verbose         Enable verbose output
  --allow-absolute      Allow absolute path references like [ref](/path/to/file.md)
```

[![CI/CD](https://github.com/flumi3/refcheck/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/flumi3/refcheck/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/flumi3/refcheck/graph/badge.svg)](https://codecov.io/gh/flumi3/refcheck)
[![Downloads](https://static.pepy.tech/badge/refcheck)](https://pepy.tech/project/refcheck)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## Installation

RefCheck is available on PyPI:

```bash
pip install refcheck
```

## Examples

```text
$ refcheck README.md

[+] 1 Markdown files to check.
- README.md

[+] FILE: README.md...
README.md:3: #introduction - OK
README.md:5: #installation - OK
README.md:6: #getting-started - OK

Reference check complete.

============================| Summary |=============================
🎉 No broken references!
====================================================================
```

```text
$ refcheck . --check-remote

[+] Searching for markdown files in C:\Users\flumi3\github\refcheck ...

[+] 2 Markdown files to check.
- tests\sample_markdown.md
- docs\Understanding-Markdown-References.md

[+] FILE: tests\sample_markdown.md...
tests\sample_markdown.md:39: /img/image.png - BROKEN
tests\sample_markdown.md:52: https://www.openai.com/logo.png - BROKEN

[+] FILE: docs\Understanding-Markdown-References.md...
docs\Understanding-Markdown-References.md:42: #local-file-references - OK

Reference check complete.

============================| Summary |=============================
[!] 2 broken references found:
tests\sample_markdown.md:39: /img/image.png
tests\sample_markdown.md:52: https://www.openai.com/logo.png
====================================================================
```

## Features

- Find and check various reference patterns in Markdown files
- Highlight broken references
- Validate absolute and relative file paths to any file type
- Support for checking remote references, such as \[Google\]\(<https://www.google.com>)
- User friendly CLI
- Easy CI pipeline integration - perfect for ensuring the quality of your Wiki

## Pre-commit Hook

RefCheck is also available as pre-commit hook!

```yaml
- repo: https://github.com/flumi3/refcheck
  rev: v0.3.0
  hooks:
    - id: refcheck
      args: ["docs/", "-e", "docs/filetoexclude.md"] # e.g. scan the docs/ folder and exclude a file
```

## Contributing

### Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning. Your commit
messages must follow this format:

```text
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types that trigger version bumps:**

- `feat:` - New feature → **minor** version bump (0.1.0 → 0.2.0)
- `fix:` - Bug fix → **patch** version bump (0.1.0 → 0.1.1)
- `perf:` - Performance improvement → **patch** version bump
- `BREAKING CHANGE:` footer or `!` after type → **major** version bump (0.1.0 → 1.0.0)

**Types that don't trigger releases:**

- `docs:` - Documentation only
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes
- `style:` - Code style/formatting
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests

**Examples:**

```bash
feat: add support for remote URL validation
fix: handle empty markdown files gracefully
docs: update installation instructions
feat!: change CLI argument format
```

### Getting Started

1. Install Poetry

   ```bash
   pipx install poetry
   ```

2. Make Poetry install virtual environments in project root

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. Install dependencies and pre-commit hooks

   ```bash
   make init
   ```

4. Run refcheck

   ```bash
   poetry run refcheck
   ```

### Development Commands

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

### Use Poetry for publishing to PyPI

1. [Create an API token](https://pypi.org/manage/account/publishing/) for authenticating to the PyPI project.

2. Configure Poetry to authenticate with PyPI:

   ```bash
   poetry config pypi-token.pypi YOUR_PYPI_API_TOKEN
   ```

3. Build the package:

   ```bash
   Poetry build
   ```

4. Publish to PyPI:

   ```bash
   Poetry publish
   ```
