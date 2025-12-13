# RefCheck Examples

This guide provides real-world examples and common usage patterns for RefCheck.

## Table of Contents

- [Basic Examples](#basic-examples)
- [Documentation Projects](#documentation-projects)
- [CI/CD Examples](#cicd-examples)
- [Advanced Patterns](#advanced-patterns)
- [Real-World Scenarios](#real-world-scenarios)

## Basic Examples

### Check a Single File

The simplest use case - validate references in one Markdown file:

```bash
refcheck README.md
```

**Output**:

```text
[+] 1 Markdown files to check.
- README.md

[+] FILE: README.md...
README.md:10: docs/guide.md - OK
README.md:15: #installation - OK
README.md:20: https://example.com - SKIPPED

Reference check complete.

============================| Summary |=============================
🎉 No broken references!
====================================================================
```

### Check Multiple Files

Validate several Markdown files at once:

```bash
refcheck README.md CONTRIBUTING.md docs/guide.md
```

### Check a Directory Recursively

Find and check all Markdown files in a directory:

```bash
refcheck docs/
```

RefCheck will:

1. Recursively search `docs/` for `.md` files
2. Validate all references in each file
3. Report broken references with file and line numbers

### Check Current Directory

Validate all Markdown files in the current directory and subdirectories:

```bash
refcheck .
```

## Documentation Projects

### Standard Documentation Structure

For a typical project with documentation:

```text
my-project/
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── getting-started.md
│   ├── api/
│   │   └── reference.md
│   └── guides/
│       ├── installation.md
│       └── configuration.md
└── examples/
    └── tutorial.md
```

**Check all documentation**:

```bash
refcheck README.md CONTRIBUTING.md docs/ examples/
```

**Or simply**:

```bash
refcheck .
```

### Exclude Generated Documentation

If you have auto-generated docs (e.g., API docs), exclude them:

```bash
refcheck docs/ -e docs/api/ docs/generated/
```

## CI/CD Examples

### GitHub Actions - Pull Request Validation

Check only Markdown files in pull requests:

```yaml
# .github/workflows/docs-check.yml
name: Documentation Check

on:
  pull_request:
    paths:
      - "**.md"

jobs:
  refcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install RefCheck
        run: pip install refcheck

      - name: Check documentation
        run: refcheck . -e node_modules/ vendor/ --no-color
```

### GitLab CI - Documentation Pipeline

```yaml
# .gitlab-ci.yml
refcheck:
  image: python:3.11-slim
  stage: test
  before_script:
    - pip install refcheck
  script:
    - refcheck docs/ README.md --no-color
  only:
    changes:
      - "**.md"
  except:
    - tags
```

### Azure DevOps Pipelines - Documentation Check

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - "**.md"

pr:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - "**.md"

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.11"
    displayName: "Set up Python"

  - script: pip install refcheck
    displayName: "Install RefCheck"

  - script: refcheck . -e node_modules/ vendor/ --no-color
    displayName: "Check documentation references"

  - script: refcheck . --check-remote --no-color -e node_modules/
    displayName: "Full validation with remote URLs (optional)"
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
```

**Explanation**:

- **trigger**: Runs on pushes to main and develop branches with markdown changes
- **pr**: Validates pull requests with markdown modifications
- **UsePythonVersion**: Sets up Python 3.11
- **check-remote**: Optional step that only runs on main branch to check external URLs

**For pull request validation only**:

```yaml
# azure-pipelines.yml (minimal)
trigger: none

pr:
  branches:
    include:
      - main
  paths:
    include:
      - "**.md"

pool:
  vmImage: "ubuntu-latest"

jobs:
  - job: CheckDocs
    displayName: "Validate Documentation"
    steps:
      - task: UsePythonVersion@0
        inputs:
          versionSpec: "3.11"

      - script: pip install refcheck
        displayName: "Install RefCheck"

      - script: refcheck . --no-color -e node_modules/ vendor/
        displayName: "Check markdown references"
```

### Pre-commit Hook - Local Validation

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/flumi3/refcheck
    rev: v0.3.0
    hooks:
      - id: refcheck
        args: ["docs/", "README.md"]
```

**Usage**:

```bash
# Install hook
pre-commit install

# Run manually
pre-commit run refcheck .

# Runs automatically on git commit
git commit -m "docs: update installation guide"
```

### Scheduled Full Validation

Weekly check including remote URLs:

```yaml
# .github/workflows/weekly-docs.yml
name: Weekly Documentation Audit

on:
  schedule:
    - cron: "0 0 * * 0" # Sunday midnight
  workflow_dispatch:

jobs:
  full-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install RefCheck
        run: pip install refcheck

      - name: Full validation with remote URLs
        run: refcheck . --check-remote --no-color -e node_modules/

      - name: Create issue if failed
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '📚 Broken documentation links detected',
              body: 'The weekly documentation audit found broken references. Please review and fix.',
              labels: ['documentation', 'maintenance']
            })
```

## Advanced Patterns

### Check Only Changed Files

Useful for large projects - only validate files modified in current branch:

```bash
# Get changed Markdown files
CHANGED_MD_FILES=$(git diff --name-only main...HEAD | grep '\.md$' || true)

# Check only if there are changed files
if [ -n "$CHANGED_MD_FILES" ]; then
    refcheck $CHANGED_MD_FILES
else
    echo "No Markdown files changed"
fi
```

### Integration with Make

Create convenient make targets:

```makefile
# Makefile
.PHONY: check-docs
check-docs:
 @echo "Checking documentation references..."
 @refcheck docs/ README.md

.PHONY: check-docs-full
check-docs-full:
 @echo "Full documentation check (including remote URLs)..."
 @refcheck . --check-remote -e node_modules/ vendor/

.PHONY: check-docs-changed
check-docs-changed:
 @echo "Checking only changed documentation..."
 @git diff --name-only main...HEAD | grep '\.md$$' | xargs -r refcheck
```

**Usage**:

```bash
make check-docs
make check-docs-full
make check-docs-changed
```

## Real-World Scenarios

### Scenario 1: Open Source Project Maintenance

**Goal**: Ensure documentation quality for contributors

**Setup**:

1. Pre-commit hook for immediate feedback
2. PR validation in CI
3. Weekly full check including remote URLs

**Pre-commit** (`.pre-commit-config.yaml`):

```yaml
repos:
  - repo: https://github.com/flumi3/refcheck
    rev: v0.3.0
    hooks:
      - id: refcheck
        args: ["docs/", "README.md", "CONTRIBUTING.md"]
```

**PR Check** (`.github/workflows/pr-docs.yml`):

```yaml
name: PR Documentation Check
on: [pull_request]
jobs:
  refcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install refcheck
      - run: refcheck . -e node_modules/ --no-color
```

**Weekly Check** (`.github/workflows/weekly.yml`):

```yaml
name: Weekly Docs Audit
on:
  schedule:
    - cron: "0 0 * * 0"
jobs:
  refcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install refcheck
      - run: refcheck . --check-remote --no-color
```

### Scenario 2: Documentation Website

**Goal**: Validate documentation before deployment

**Tech Stack**: MkDocs + GitHub Pages

**Workflow**:

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Documentation

on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install mkdocs-material refcheck

      - name: Validate references
        run: refcheck docs/ -e docs/generated/ --no-color

      - name: Build documentation
        run: mkdocs build

      - name: Deploy to GitHub Pages
        if: success()
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## Tips and Tricks

### Tip 1: Create Aliases

Add to your shell profile (`.bashrc`, `.zshrc`):

```bash
# Quick documentation check
alias check-docs='refcheck docs/ README.md'

# Full check with remote
alias check-docs-full='refcheck . --check-remote --no-color'

# Check changed docs
alias check-docs-changed='git diff --name-only | grep "\.md$" | xargs -r refcheck'
```

### Tip 2: VS Code Task

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "RefCheck Documentation",
      "type": "shell",
      "command": "refcheck",
      "args": ["docs/", "README.md"],
      "problemMatcher": [],
      "group": "test"
    }
  ]
}
```

Run with `Cmd/Ctrl + Shift + P` → `Tasks: Run Task` → `RefCheck Documentation`

### Tip 3: Integration with Documentation Generators

**With Sphinx**:

```bash
# In Makefile or build script
refcheck source/ && sphinx-build -b html source/ build/
```

**With Docusaurus**:

```bash
# In package.json scripts
{
  "scripts": {
    "docs:check": "refcheck docs/",
    "docs:build": "npm run docs:check && docusaurus build"
  }
}
```

## Next Steps

- See [CLI Reference](CLI-Reference.md) for all available options
- Check [Integration Guide](Integration-Guide.md) for CI/CD setup
