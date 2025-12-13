# Integration Guide

This guide shows you how to integrate RefCheck into your development workflows, CI/CD pipelines, and automated
processes.

## Table of Contents

- [Pre-commit Hooks](#pre-commit-hooks)
- [Makefile Integration](#makefile-integration)

## Pre-commit Hooks

Pre-commit hooks provide the fastest feedback by validating references before code is committed.

### Using pre-commit Framework

RefCheck is available as a [pre-commit](https://pre-commit.com/) hook.

#### 1. Install pre-commit

```bash
pip install pre-commit
# or
pipx install pre-commit  # recommended
```

#### 2. Add to `.pre-commit-config.yaml`

Create or update `.pre-commit-config.yaml` in your repository root:

```yaml
repos:
  - repo: https://github.com/flumi3/refcheck
    rev: v0.3.0 # Use the latest version
    hooks:
      - id: refcheck
        args: ["docs/"] # Specify paths to check
```

#### 3. Install the hook

```bash
pre-commit install
```

#### 4. (Optional) Run manually

```bash
# Check all files in the current directory
pre-commit run refcheck .

# Check specific files
pre-commit run refcheck --files README.md docs/guide.md
```

### Advanced Pre-commit Configuration

#### Check Multiple Directories

```yaml
- repo: https://github.com/flumi3/refcheck
  rev: v0.3.0
  hooks:
    - id: refcheck
      args: ["docs/", "README.md", "CONTRIBUTING.md"]
```

#### Exclude Files

```yaml
- repo: https://github.com/flumi3/refcheck
  rev: v0.3.0
  hooks:
    - id: refcheck
      args:
        - "docs/"
        - "-e"
        - "docs/archive/"
        - "docs/generated/"
```

#### Check Only Staged Markdown Files

```yaml
- repo: https://github.com/flumi3/refcheck
  rev: v0.3.0
  hooks:
    - id: refcheck
      files: '\.md$' # Only run on .md files
```

## Makefile Integration

Add to your `Makefile`:

```makefile
.PHONY: check-docs
check-docs:
 @echo "Checking Markdown references..."
 @refcheck docs/ README.md

.PHONY: check-docs-full
check-docs-full:
 @echo "Full documentation check (including remote URLs)..."
 @refcheck docs/ --check-remote
```

Usage:

```bash
make check-docs
make check-docs-full
```
