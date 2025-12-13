# Development Guide

## Project Overview

RefCheck is a Markdown reference validator that detects broken links, file references, and header anchors. It's a CLI
tool distributed via PyPI, designed for CI/CD integration and pre-commit hooks.

## Architecture & Data Flow

### Core Pipeline (main.py)

1. **Settings** → CLI args parsed via `argparse` in [cli.py](../refcheck/cli.py), exposed as singleton `settings` in
   [settings.py](../refcheck/settings.py)
2. **File Discovery** → `get_markdown_files_from_args()` in [utils.py](../refcheck/utils.py) collects `.md` files
   respecting `--exclude`
3. **Parsing** → `MarkdownParser` extracts references using regex patterns, filters out code blocks
4. **Validation** → `ReferenceChecker` validates each reference, categorizing as local/remote
5. **Reporting** → Aggregates broken refs, prints summary with colored output

### Key Components

**Reference Extraction ([parsers.py](../refcheck/parsers.py))**

- Uses distinct regex patterns for different reference types: `BASIC_REFERENCE_PATTERN`, `INLINE_LINK_PATTERN`,
  `HTML_IMAGE_PATTERN`
- **Critical**: Code blocks and inline code are extracted first and used to filter out false positives
- Returns dict with keys: `basic_references`, `basic_images`, `inline_links`

**Validation Logic ([validators.py](../refcheck/validators.py))**

- `file_exists()`: Handles 3 path types:
  - Simple relative (e.g., `../file.md`)
  - Backslash-prefixed Windows-style (treated as relative)
  - Absolute (`/file.md`) - requires `--allow-absolute` flag, searches up directory tree
- `is_valid_markdown_reference()`: Validates `.md` files and header anchors (e.g., `file.md#section`)
- Remote checks use `requests.head()` with 5s timeout, disabled SSL verification

**Settings Singleton ([settings.py](../refcheck/settings.py))**

- Properties only (no setters), initialized once from CLI args
- **Important**: Returns empty defaults when running under pytest (checks `"pytest" in sys.modules`)

## Development Commands (Makefile)

**Quality Assurance (always run before commits)**:

```bash
make qa          # Format, lint, type-check, dead code, unused deps
make format      # Ruff auto-format
make lint        # Ruff linting with --fix
make check-types # MyPy type checking
```

**Testing**:

```bash
make test        # Run pytest with coverage
make test-cov    # Generate HTML coverage report
```

**Setup**:

```bash
make init        # Install deps + pre-commit hooks
```

## Testing Patterns

**Fixture Usage**: Heavy use of `unittest.mock` for patching OS and settings:

```python
@pytest.fixture
def mock_settings_absolute_path():
    with mock.patch("refcheck.validators.settings") as mock_settings:
        mock_settings.allow_absolute = True
        yield mock_settings
```

**Test Organization**: Validators have dedicated test directories (e.g., `tests/test_validators/`)

## Project Conventions

**Path Handling**: All file operations use `os.path` (not `pathlib`), normalize paths with `os.path.abspath()`

**Logging**: Use module-level `logger = logging.getLogger()`, setup via `log_conf.py`

**Color Output**: Utility functions in [utils.py](../refcheck/utils.py): `print_red()`, `print_green()`,
`print_yellow()` - respect `settings.no_color`

**Error Handling**: Broad try-except for file I/O, requests use `requests.exceptions.RequestException`

**Regex Patterns**: Define at module level as compiled patterns (e.g., `CODE_BLOCK_PATTERN = re.compile(...)`)

## Dependency Management

- **Poetry** for package management (`pyproject.toml`)
- **Ruff** for formatting + linting (line length: 100)
- **MyPy** for type checking (permissive: `disallow_untyped_defs = false`)
- **Vulture** for dead code detection (min confidence: 80, see ignore list in `pyproject.toml`)
- **Deptry** for unused dependency detection

## CI/CD & Release

- Semantic versioning via `python-semantic-release` (Angular commit convention)
- Version tracked in: `pyproject.toml`, `README.md` (pre-commit hook ref)
- Commitizen enforces conventional commits
- Pre-commit hooks: commit-msg validation + pre-push QA checks

## Common Gotchas

1. **Absolute Paths**: `/file.md` is NOT treated as root unless `--allow-absolute` is set - it searches up directory
   tree from origin file
2. **Windows Backslash**: `\file.md` is treated as relative (removes leading backslash)
3. **Code Block Filtering**: References inside ` ```...``` ` or `` `...` `` are intentionally ignored
4. **Remote Checks**: Default OFF - must use `--check-remote` flag
5. **Settings in Tests**: Settings object returns empty defaults when pytest is running

## Adding New Reference Types

1. Add regex pattern to [parsers.py](../refcheck/parsers.py) (e.g., `NEW_PATTERN = re.compile(...)`)
2. Extract matches in `parse_markdown_file()` using `_find_matches_with_line_numbers()`
3. Filter code blocks: `_drop_code_references(matches, all_code)`
4. Process to `Reference` objects: `_process_basic_references()` or custom processor
5. Add validation logic to [validators.py](../refcheck/validators.py) or handle in `ReferenceChecker.check_references()`
6. Add comprehensive tests in `tests/test_validators/`
