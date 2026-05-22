# CLI Reference

```text
refcheck [OPTIONS] [PATH ...]
```

## Arguments

| Argument | Description                                                                                               |
| -------- | --------------------------------------------------------------------------------------------------------- |
| `PATH`   | One or more Markdown files or directories to check. Directories are searched recursively for `.md` files. |

## Options

| Option                  | Description                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| `-h`, `--help`          | Show help message and exit.                                                                                   |
| `-e`, `--exclude [...]` | Exclude files or directories from checking.                                                                   |
| `-cm`, `--check-remote` | Validate remote HTTP/HTTPS URLs (skipped by default). Uses HEAD requests with a 5s timeout.                   |
| `-nc`, `--no-color`     | Disable colored output. Useful for CI/CD or redirecting to files.                                             |
| `-v`, `--verbose`       | Enable verbose logging (file parsing details, validation steps, HTTP info).                                   |
| `--allow-absolute`      | Allow absolute path references like `/docs/file.md`. Without this flag, absolute paths are flagged as broken. |

## Exit Codes

| Code | Meaning                                          |
| ---- | ------------------------------------------------ |
| `0`  | No broken references found.                      |
| `1`  | Broken references detected or invalid arguments. |

## Examples

```bash
# Check a single file
refcheck README.md

# Check a directory recursively
refcheck docs/

# Exclude files or directories
refcheck docs/ -e docs/archive/ docs/draft.md

# Full validation including remote URLs
refcheck docs/ --check-remote

# CI-friendly output
refcheck docs/ --no-color
```
