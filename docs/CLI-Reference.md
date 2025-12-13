# CLI Reference

This guide provides a complete reference for RefCheck's command-line interface, including all options, flags, and usage
patterns.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Command Syntax](#command-syntax)
- [Options Reference](#options-reference)
  - [-h, --help](#-h---help)
  - [-e, --exclude](#-e---exclude-)
  - [-cm, --check-remote](#-cm---check-remote)
  - [-nc, --no-color](#-nc---no-color)
  - [-v, --verbose](#-v---verbose)
  - [--allow-absolute](#--allow-absolute)
- [Exit Codes](#exit-codes)
- [Usage Patterns](#usage-patterns)
- [Best Practices](#best-practices)

## Basic Usage

The most basic usage of RefCheck is to check a single Markdown file or directory:

```bash
# Check a single file
refcheck README.md

# Check a directory (recursively finds all .md files)
refcheck docs/

# Check multiple paths
refcheck README.md docs/ guides/
```

## Command Syntax

```text
refcheck [OPTIONS] [PATH ...]
```

### Arguments

- `PATH` - One or more Markdown files or directories to check
  - Accepts file paths: `README.md`, `docs/guide.md`
  - Accepts directories: `docs/`, `.` (current directory)
  - Multiple paths can be specified: `refcheck file1.md file2.md docs/`
  - Directories are searched recursively for `.md` files

## Options Reference

### `-h, --help`

Display help message and exit.

```bash
refcheck --help
```

Shows:

- Command syntax
- Available options
- Brief description of each option

---

### `-e, --exclude [...]`

Exclude specific files or directories from checking.

**Syntax:**

```bash
refcheck [PATH] -e [EXCLUDE_PATTERNS ...]
```

**Examples:**

```bash
# Exclude a single file
refcheck docs/ -e docs/draft.md

# Exclude multiple files
refcheck docs/ -e docs/draft.md docs/archive.md

# Exclude entire directories
refcheck . -e node_modules/ vendor/

# Exclude with patterns
refcheck docs/ -e docs/archive/ docs/deprecated.md
```

**Notes:**

- Exclusion paths can be relative or absolute
- Directories are excluded recursively
- Multiple exclusions are separated by spaces

---

### `-cm, --check-remote`

Enable validation of remote HTTP/HTTPS URLs.

**Syntax:**

```bash
refcheck [PATH] --check-remote
```

**Examples:**

```bash
# Check local and remote references
refcheck README.md --check-remote

# Check all docs with remote validation
refcheck docs/ -cm
```

**Behavior:**

- Without this flag: Remote URLs are **skipped** with a warning
- With this flag: Remote URLs are validated via HTTP HEAD requests
- Validates status codes (anything < 400 is considered OK)
- Times out after 5 seconds per URL
- SSL verification is disabled by default

**Performance Note:** Remote checking can be slow if your documentation has many external links. Consider using this
selectively:

- In pre-commit hooks: Skip remote checks for speed
- In CI/CD pipelines: Enable for thorough validation

---

### `-nc, --no-color`

Disable colored output.

**Syntax:**

```bash
refcheck [PATH] --no-color
```

**Examples:**

```bash
# Plain text output
refcheck README.md --no-color

# Useful for logs and CI environments
refcheck docs/ -nc > validation-report.txt
```

**Use Cases:**

- CI/CD pipelines that don't support ANSI colors
- Redirecting output to files
- Terminal emulators without color support
- Automated parsing of output

---

### `-v, --verbose`

Enable verbose logging output.

**Syntax:**

```bash
refcheck [PATH] --verbose
```

**Examples:**

```bash
# See detailed processing information
refcheck README.md --verbose

# Debug reference validation
refcheck docs/ -v
```

**Output Includes:**

- File parsing details
- Reference extraction information
- Validation steps for each reference
- Error details and stack traces
- HTTP request/response information (with `--check-remote`)

**Logging Levels:**

- Without `-v`: Shows only errors and summary
- With `-v`: Shows info, warnings, and detailed processing

---

### `--allow-absolute`

Allow absolute path references in Markdown files.

**Syntax:**

```bash
refcheck [PATH] --allow-absolute
```

**Examples:**

```bash
# Allow references like [link](/absolute/path.md)
refcheck docs/ --allow-absolute
```

**Behavior:**

By default, RefCheck treats absolute paths (starting with `/`) as potentially broken because they may not resolve
correctly in different environments.

- **Without flag**: `[link](/docs/file.md)` is flagged as potentially broken
- **With flag**: `[link](/docs/file.md)` is validated as an absolute path from the root

**When to Use:**

- Your documentation uses absolute paths from a known root
- Working with documentation that will be served from a web root
- Dealing with legacy documentation that uses absolute references

**When to Avoid:**

- Portable documentation that should work in any environment
- Documentation that may be viewed locally or in different contexts
- Following best practices (prefer relative paths)

## Exit Codes

RefCheck uses standard exit codes for integration with scripts and CI/CD pipelines:

| Exit Code | Meaning | Description                                     |
| --------- | ------- | ----------------------------------------------- |
| `0`       | Success | No broken references found                      |
| `1`       | Failure | Broken references detected OR invalid arguments |

**Examples:**

```bash
# Check exit code in a script
refcheck docs/
if [ $? -eq 0 ]; then
    echo "All references are valid!"
else
    echo "Broken references found!"
    exit 1
fi

# In GitHub Actions
- name: Check documentation
  run: refcheck docs/
  # Fails the workflow if exit code is non-zero
```

## Usage Patterns

### Common Workflows

#### 1. Check Current Directory

```bash
# Check all Markdown files in current directory and subdirectories
refcheck .
```

#### 2. Check Specific Documentation Folder

```bash
# Focus on documentation directory
refcheck docs/
```

#### 3. Check with Exclusions

```bash
# Exclude generated files and archives
refcheck docs/ -e docs/generated/ docs/archive/
```

#### 4. Full Validation (Local + Remote)

```bash
# Comprehensive check including remote URLs
refcheck docs/ --check-remote
```

#### 5. Verbose Debugging

```bash
# Troubleshoot reference validation issues
refcheck problematic-file.md --verbose
```

#### 6. CI/CD Pipeline

```bash
# Fast check for CI (skip remote, no color)
refcheck docs/ --no-color

# Thorough check for nightly builds
refcheck . --check-remote --no-color -e node_modules/ vendor/
```

#### 7. Pre-commit Validation

```bash
# Quick local check of staged files
refcheck README.md docs/ -e docs/drafts/
```

### Combining Options

RefCheck options can be combined for sophisticated workflows:

```bash
# Full validation with verbose output, no colors, exclude archives
refcheck docs/ \
  --check-remote \
  --verbose \
  --no-color \
  -e docs/archive/ docs/deprecated/
```

```bash
# Allow absolute paths, check remotes, but exclude node_modules
refcheck . \
  --allow-absolute \
  --check-remote \
  -e node_modules/ .git/ build/
```

### Output Redirection

```bash
# Save report to file
refcheck docs/ --no-color > refcheck-report.txt

# Append to log
refcheck docs/ --no-color >> validation-log.txt 2>&1

# Both stdout and stderr
refcheck docs/ --verbose &> full-output.log
```

## Best Practices

### 1. **Use in CI/CD Pipelines**

```bash
# Fast check without remote validation
refcheck docs/ --no-color
```

**Rationale:** Skip remote checks for faster feedback in pull requests. Use separate scheduled jobs for full validation.

### 2. **Exclude Generated Files**

```bash
refcheck docs/ -e docs/api/ docs/generated/
```

**Rationale:** Auto-generated documentation may have different validation requirements or be rebuilt frequently.

**Rationale:** Catch broken references before they enter the repository.

### 3. **Verbose Mode for Debugging**

```bash
# Use verbose when investigating issues
refcheck problematic-file.md --verbose
```

**Rationale:** Detailed output helps diagnose why a reference is flagged as broken.

### 4. **Separate Remote Validation**

```bash
# Regular check
refcheck docs/

# Periodic full check (e.g., nightly)
refcheck docs/ --check-remote
```

**Rationale:** Remote validation is slower and URLs may be temporarily unavailable. Separate concerns for better
workflow.

### 5. **Consistent Exclusions**

Create a script or configuration for repeated exclusions:

```bash
#!/bin/bash
# check-docs.sh
refcheck docs/ -e docs/archive/ docs/generated/ docs/drafts/
```

**Rationale:** Maintain consistency across manual checks and automation.

## Examples

See [Examples.md](Examples.md) for real-world usage scenarios and advanced patterns.
