# Integration Guide

## Pre-commit Hook

RefCheck is available as a [pre-commit](https://pre-commit.com/) hook:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/flumi3/refcheck
    rev: v0.5.0
    hooks:
      - id: refcheck
        args: ["docs/", "README.md", "-e", "docs/archive/"]
```

```bash
# Install the hook
pre-commit install

# Run manually
pre-commit run refcheck .
```

## GitHub Actions

Validate documentation references on pull requests:

```yaml
# .github/workflows/docs-check.yml
name: Documentation Check

on:
  pull_request:
    paths: ["**.md"]

jobs:
  refcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install refcheck
      - run: refcheck . --no-color -e node_modules/
```

For thorough validation including remote URLs, consider a scheduled weekly run:

```yaml
# .github/workflows/weekly-docs.yml
name: Weekly Documentation Audit

on:
  schedule:
    - cron: "0 0 * * 0"

jobs:
  refcheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install refcheck
      - run: refcheck . --check-remote --no-color
```

## Azure DevOps Pipelines

Validate documentation references in Azure DevOps pull request builds:

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pr:
  paths:
    include:
      - "**.md"

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.11"

  - script: pip install refcheck
    displayName: "Install RefCheck"

  - script: refcheck . --no-color -e node_modules/
    displayName: "Check Markdown references"
```

For a scheduled pipeline that also validates remote URLs:

```yaml
# azure-pipelines-weekly-docs.yml
schedules:
  - cron: "0 0 * * 0"
    displayName: "Weekly documentation audit"
    branches:
      include:
        - main
    always: true

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.11"

  - script: pip install refcheck
    displayName: "Install RefCheck"

  - script: refcheck . --check-remote --no-color
    displayName: "Check Markdown references (including remote)"
```

## Makefile

```makefile
.PHONY: check-docs
check-docs:
 @refcheck docs/ README.md --no-color

.PHONY: check-docs-full
check-docs-full:
 @refcheck docs/ README.md --check-remote --no-color
```
