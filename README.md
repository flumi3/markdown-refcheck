# Markdown RefCheck

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/refcheck?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=ORANGE&left_text=downloads)](https://pepy.tech/projects/refcheck)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-silver.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/flumi3/markdown-refcheck/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/flumi3/markdown-refcheck/actions/workflows/ci-cd.yml)

Markdown RefCheck is a simple tool that checks Markdown references to find any broken links. It
helps keeping your documentation free from broken section refs, missing images and files, and
unavailable website links.

## Features

- 🔍 **Reference Detection** — Validate links, images, file refs, and header anchors
- 🌐 **Remote URL Checking** — Validate external HTTP/HTTPS links (optional)
- 💬 **Inline Ignore Comments** — Suppress false positives with
  [`<!-- refcheck-ignore -->`](docs/user-guide/Ignoring-References.md) directives
- ⚙️ **CI/CD Ready** — Exit codes and `--no-color` for automation
- 🚀 **Pre-commit Integration** — Available as a
  [pre-commit hook](docs/user-guide/Integration-Guide.md#pre-commit-hook)

## Installation

```bash
pip install refcheck
# or
pipx install refcheck
```

## Quick Start

```bash
# Check a single file
refcheck README.md

# Check a directory recursively
refcheck docs/

# Include remote URL validation
refcheck docs/ --check-remote
```

**Example output:**

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

For all CLI options, see the [CLI Reference](docs/user-guide/CLI-Reference.md).

## Pre-commit

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/flumi3/refcheck
  rev: v0.6.0
  hooks:
    - id: refcheck
      args: ["docs/", "--exclude", "docs/filetoexclude.md"]
```

See the [Integration Guide](docs/user-guide/Integration-Guide.md) for CI/CD and other workflow
setups.

## Documentation

- [CLI Reference](docs/user-guide/CLI-Reference.md) — Command-line options
- [Ignoring References](docs/user-guide/Ignoring-References.md) — Suppress false positives
- [Integration Guide](docs/user-guide/Integration-Guide.md) — Pre-commit, CI/CD, Azure DevOps,
  Makefile
- [Development Guide](docs/developer-guide/Development-Guide.md) — Architecture, setup, conventions

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).
