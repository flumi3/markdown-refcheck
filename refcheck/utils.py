import os
import logging

from refcheck.settings import settings

logger = logging.getLogger()

IGNORE_FILE = ".refcheckignore"

CHECK_IGNORE_DEFAULTS = [
    ".git/",
    ".vscode/",
    ".idea/",
    "__pycache__/",
    "node_modules/",
    "venv/",
    ".venv/",
    ".pytest_cache/",
]


def load_exclusion_patterns() -> list[str]:
    """Read exclusions from the .refcheckignore file."""
    if not os.path.isfile(IGNORE_FILE):
        logger.info(f"Could not find {IGNORE_FILE}. Using default exclusions.")
        exclusions = CHECK_IGNORE_DEFAULTS
    else:
        logger.info(f"Reading exclusions from {IGNORE_FILE}...")
        with open(IGNORE_FILE, "r", encoding="utf-8") as file:
            exclusions = [line.strip() for line in file if line.strip()]

    ui_print(
        f"[!] WARNING: Skipping these files and directories: {exclusions}", color_fn=print_yellow
    )
    return exclusions


def _is_path_excluded(path: str, exclude_set: set[str]) -> bool:
    """Check if a path should be excluded based on the exclude set.

    Handles both bare names (e.g. 'node_modules') that may appear anywhere in the
    path tree, and explicit relative/absolute paths (e.g. '../some/dir').
    """
    for ex in exclude_set:
        if path == ex or path.startswith(ex + os.sep):
            return True
        # Bare name with no separator: match against individual path components
        if os.sep not in ex and ex in path.split(os.sep):
            return True
    return False


def get_markdown_files_from_dir(root_dir: str, exclude: list[str] | None = None) -> list[str]:
    """Traverse the directory to get all markdown files."""
    if exclude is None:
        exclude = []
    ui_print(f"[+] Searching for markdown files in {os.path.abspath(root_dir)} ...")
    exclude_set = set(os.path.normpath(path) for path in exclude)
    markdown_files = []

    # Walk through the directory to get all markdown files
    for subdir, _, files in os.walk(root_dir):
        subdir_norm = os.path.normpath(subdir)
        if _is_path_excluded(subdir_norm, exclude_set):
            continue  # Skip excluded directories

        for file in files:
            file_path = os.path.join(subdir, file)
            file_path_norm = os.path.normpath(file_path)
            if file.endswith(".md") and file_path_norm not in exclude_set:
                markdown_files.append(file_path_norm)

    return markdown_files


def get_markdown_files_from_args(paths: list[str], exclude: list[str] | None = None) -> list[str]:
    """Retrieve all markdown files specified by the user."""
    # Read additional exclusions from the ignore file
    if exclude is None:
        exclude = []
    exclude += load_exclusion_patterns()

    exclude_set = set(os.path.normpath(path) for path in exclude)
    markdown_files = set()

    for path in paths:
        norm_path = os.path.normpath(path)
        if norm_path in exclude_set:
            continue
        if os.path.isdir(norm_path):
            markdown_files.update(get_markdown_files_from_dir(norm_path, exclude))
        elif os.path.isfile(norm_path):
            if norm_path.endswith(".md"):
                markdown_files.add(norm_path)
        else:
            ui_print(
                f"[!] Warning: {path} is not a valid file or directory.", color_fn=print_yellow
            )

    return list(markdown_files)


# ---------------------------------------------------------------------------
# UI helper – centralised printing respecting the ``--quiet`` flag
# ---------------------------------------------------------------------------
def ui_print(message: str, *, color_fn=None, end: str = "\n") -> None:
    """Print *message* only when the CLI is **not** in quiet mode.

    If *color_fn* is provided, it will be applied to the message before printing.
    Color functions (e.g., print_red, print_yellow) automatically respect the
    ``--no-color`` flag, so the message will either be colorized or plain text.

    The function defensively checks for the ``quiet`` attribute using ``getattr``
    so that unit tests which replace ``refcheck.utils.settings`` with a mock
    (which may not define ``quiet``) still behave correctly.
    """
    # Apply color function if provided
    if color_fn is not None:
        message = color_fn(message)

    # ``settings.quiet`` may be a MagicMock in tests; only suppress output when the
    # attribute is explicitly ``True``.
    if getattr(settings, "quiet", False) is not True:
        print(message, end=end)


def print_green_background(text: str) -> str:
    return text if settings.no_color else f"\033[42m{text}\033[0m"


def print_red_background(text: str) -> str:
    return text if settings.no_color else f"\033[41m{text}\033[0m"


def print_red(text: str) -> str:
    return text if settings.no_color else f"\033[31m{text}\033[0m"


def print_green(text: str) -> str:
    return text if settings.no_color else f"\033[32m{text}\033[0m"


def print_yellow(text: str) -> str:
    return text if settings.no_color else f"\033[33m{text}\033[0m"
