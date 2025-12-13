"""Shared test fixtures and mocks for RefCheck tests."""

import pytest
import requests
from unittest import mock


# ============================================================================
# Settings Fixtures
# ============================================================================


@pytest.fixture
def mock_settings_default():
    """Mock settings with default values."""
    with (
        mock.patch("refcheck.validators.settings") as mock_settings_validators,
        mock.patch("refcheck.parsers.settings") as mock_settings_parsers,
        mock.patch("refcheck.utils.settings") as mock_settings_utils,
        mock.patch("refcheck.main.settings") as mock_settings_main,
    ):
        for mock_settings in [
            mock_settings_validators,
            mock_settings_parsers,
            mock_settings_utils,
            mock_settings_main,
        ]:
            mock_settings.paths = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.allow_absolute = False
            mock_settings.exclude = []

        yield mock_settings_validators


@pytest.fixture
def mock_settings_remote():
    """Mock settings with remote checking enabled."""
    with mock.patch("refcheck.validators.settings") as mock_settings:
        mock_settings.paths = []
        mock_settings.verbose = False
        mock_settings.check_remote = True
        mock_settings.no_color = True
        mock_settings.allow_absolute = False
        mock_settings.exclude = []
        yield mock_settings


@pytest.fixture
def mock_settings_absolute():
    """Mock settings with absolute paths allowed."""
    with mock.patch("refcheck.validators.settings") as mock_settings:
        mock_settings.paths = []
        mock_settings.verbose = False
        mock_settings.check_remote = False
        mock_settings.no_color = True
        mock_settings.allow_absolute = True
        mock_settings.exclude = []
        yield mock_settings


@pytest.fixture
def mock_settings_verbose():
    """Mock settings with verbose mode enabled."""
    with (
        mock.patch("refcheck.validators.settings") as mock_settings_validators,
        mock.patch("refcheck.parsers.settings") as mock_settings_parsers,
        mock.patch("refcheck.utils.settings") as mock_settings_utils,
        mock.patch("refcheck.main.settings") as mock_settings_main,
    ):
        for mock_settings in [
            mock_settings_validators,
            mock_settings_parsers,
            mock_settings_utils,
            mock_settings_main,
        ]:
            mock_settings.paths = []
            mock_settings.verbose = True
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.allow_absolute = False
            mock_settings.exclude = []

        yield mock_settings_validators


# ============================================================================
# HTTP Request Fixtures
# ============================================================================


@pytest.fixture
def mock_http_success():
    """Mock successful HTTP response."""
    with mock.patch("requests.head") as mock_request:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        yield mock_request


@pytest.fixture
def mock_http_404():
    """Mock HTTP 404 Not Found response."""
    with mock.patch("requests.head") as mock_request:
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response
        yield mock_request


@pytest.fixture
def mock_http_301():
    """Mock HTTP 301 redirect response."""
    with mock.patch("requests.head") as mock_request:
        mock_response = mock.Mock()
        mock_response.status_code = 301
        mock_request.return_value = mock_response
        yield mock_request


@pytest.fixture
def mock_http_timeout():
    """Mock HTTP timeout exception."""
    with mock.patch("requests.head") as mock_request:
        mock_request.side_effect = requests.exceptions.Timeout("Request timed out")
        yield mock_request


@pytest.fixture
def mock_http_connection_error():
    """Mock HTTP connection error."""
    with mock.patch("requests.head") as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")
        yield mock_request


@pytest.fixture
def mock_http_ssl_error():
    """Mock SSL certificate error."""
    with mock.patch("requests.head") as mock_request:
        mock_request.side_effect = requests.exceptions.SSLError("SSL certificate verify failed")
        yield mock_request


# ============================================================================
# File System Fixtures
# ============================================================================


@pytest.fixture
def temp_markdown_file(tmp_path):
    """Create a temporary markdown file for testing."""

    def _create_file(content: str, filename: str = "test.md"):
        file_path = tmp_path / filename
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    return _create_file


@pytest.fixture
def temp_directory_structure(tmp_path):
    """Create a temporary directory structure with markdown files."""

    def _create_structure(structure: dict):
        """
        Create a directory structure from a dictionary.
        Example structure:
        {
            "file1.md": "content",
            "subdir": {
                "file2.md": "content"
            }
        }
        """

        def create_recursive(base_path, struct):
            for name, content in struct.items():
                path = base_path / name
                if isinstance(content, dict):
                    path.mkdir(exist_ok=True)
                    create_recursive(path, content)
                else:
                    path.write_text(content, encoding="utf-8")

        create_recursive(tmp_path, structure)
        return str(tmp_path)

    return _create_structure


@pytest.fixture
def mock_refcheckignore_exists():
    """Mock .refcheckignore file existence."""
    with mock.patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = True
        yield mock_isfile


@pytest.fixture
def mock_refcheckignore_missing():
    """Mock .refcheckignore file missing."""
    with mock.patch("os.path.isfile") as mock_isfile:
        mock_isfile.return_value = False
        yield mock_isfile


# ============================================================================
# Common Test Data
# ============================================================================


@pytest.fixture
def sample_valid_markdown():
    """Sample valid markdown content with various reference types."""
    return """# Sample Document

## Section 1

Here's a [basic link](file.md) to another document.

And an image: ![alt text](image.png)

External link: [Google](https://www.google.com)

Inline link: <https://example.com>

## Code Examples

```python
# This should be ignored
print("[fake link](ignored.md)")
```

Inline code: `[not a link](nope.md)` should also be ignored.
"""


@pytest.fixture
def sample_markdown_with_headers():
    """Sample markdown with header references."""
    return """# Main Title

## Section A

Link to [same file header](#section-b)

Link to [other file header](other.md#introduction)

## Section B

Content here.
"""


@pytest.fixture
def sample_markdown_with_code_blocks():
    """Sample markdown with code blocks containing fake references."""
    return """# Document

Normal [link](real.md) here.

```markdown
Fake [link](fake.md) in code block.
```

Another normal [link](another.md).

Inline code: `[fake](inline.md)` should be ignored.

```python
# Comment with [reference](code.md)
print("test")
```
"""
