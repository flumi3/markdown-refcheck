# Development Guide

## Setup

**Prerequisites**: Python 3.10+, [Poetry](https://python-poetry.org/)

```bash
# Configure Poetry to create venvs in-project
poetry config virtualenvs.in-project true

# Clone and initialize
git clone https://github.com/YOUR_USERNAME/refcheck.git
cd refcheck
make init    # Installs deps + pre-commit hooks

# Verify
poetry run refcheck --help
```

## Development Commands

```bash
make qa              # Format, lint, type-check, dead code, unused deps
make test            # Run tests with coverage (minimum 80%)
make test-coverage   # Tests + HTML coverage report in htmlcov/
make format          # Ruff auto-format
make lint            # Ruff linting with --fix
make check-types     # MyPy type checking
make help            # Show all available commands
```

## Architecture

### Core Pipeline

1. **CLI** → `argparse` in `cli.py`, exposed as singleton `settings` in `settings.py`
2. **File Discovery** → `get_markdown_files_from_args()` in `utils.py` collects `.md` files
   respecting `--exclude`
3. **Parsing** → `MarkdownParser` extracts references using regex patterns, filters out code blocks
4. **Validation** → `ReferenceChecker` validates each reference (local files, headers, remote URLs)
5. **Reporting** → Aggregates broken refs, prints summary with colored output

### Key Components

- **`parsers.py`** — Regex-based extraction of references. Code blocks/inline code are extracted
  first to filter false positives. Returns dict with keys: `basic_references`, `basic_images`,
  `inline_links`.
- **`validators.py`** — `file_exists()` handles relative, Windows backslash, and absolute paths.
  `is_valid_markdown_reference()` validates `.md` files and header anchors. Remote checks use
  `requests.head()` with 5s timeout.
- **`settings.py`** — Properties only (no setters), initialized once from CLI args. Returns empty
  defaults when running under pytest.

## Project Conventions

- **Path handling**: `os.path` (not `pathlib`), normalize with `os.path.abspath()`
- **Logging**: Module-level `logger = logging.getLogger()`, setup via `log_conf.py`
- **Color output**: `print_red()`, `print_green()`, `print_yellow()` in `utils.py` — respect
  `settings.no_color`
- **Regex patterns**: Defined at module level as compiled patterns
- **Error handling**: Broad try-except for file I/O, `requests.exceptions.RequestException` for HTTP

## Testing

- All new code requires tests. Minimum 80% coverage overall, aim for 90%+ on new modules.
- Validators have dedicated test directories (`tests/test_validators/`).
- Heavy use of `unittest.mock` for patching OS and settings.
- Test fixtures live in `tests/fixtures/` for realistic scenarios.

```bash
# Run specific test file
poetry run pytest tests/test_validators/test_file_exists.py

# Run tests matching a pattern
poetry run pytest -k "test_header"
```

## Tooling

| Tool        | Purpose                     | Config                          |
| ----------- | --------------------------- | ------------------------------- |
| **Poetry**  | Package management          | `pyproject.toml`                |
| **Ruff**    | Format + lint               | Line length: 100                |
| **MyPy**    | Type checking               | `disallow_untyped_defs = false` |
| **Vulture** | Dead code detection         | Min confidence: 80              |
| **Deptry**  | Unused dependency detection | —                               |

## Release Process

Automated via GitHub Actions on push to `main`:

1. `python-semantic-release` analyzes commit messages
2. Version bumped based on commit types (see
   [CONTRIBUTING.md](../../CONTRIBUTING.md#commit-convention))
3. `CHANGELOG.md` updated, git tag created
4. Package built and published to PyPI

Version tracked in: `pyproject.toml`, `README.md` (pre-commit hook ref).

## Common Gotchas

1. **Absolute paths**: `/file.md` is NOT treated as root unless `--allow-absolute` is set — it
   searches up the directory tree from the origin file.
2. **Windows backslash**: `\file.md` is treated as relative (leading backslash removed).
3. **Code block filtering**: References inside ` ```...``` ` or `` `...` `` are intentionally
   ignored.
4. **Remote checks**: Default OFF — must use `--check-remote` flag.
5. **Settings in tests**: Settings object returns empty defaults when pytest is running.

## Adding New Reference Types

1. Add regex pattern to `parsers.py` (e.g., `NEW_PATTERN = re.compile(...)`)
2. Extract matches in `parse_markdown_file()` using `_find_matches_with_line_numbers()`
3. Filter code blocks: `_drop_code_references(matches, all_code)`
4. Process to `Reference` objects: `_process_basic_references()` or custom processor
5. Add validation logic to `validators.py` or handle in `ReferenceChecker.check_references()`
6. Add comprehensive tests in `tests/test_validators/`
