# Markdown RefCheck

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/refcheck?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=ORANGE&left_text=downloads)](https://pepy.tech/projects/refcheck)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-silver.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/flumi3/markdown-refcheck/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/flumi3/markdown-refcheck/actions/workflows/ci-cd.yml)

Markdown RefCheck is a simple tool that checks Markdown references to find any broken links.  
It helps keeping your documentation free from broken section refs, missing images and files, and unavailable websites
links.

```text
usage: refcheck [OPTIONS] [PATH ...]

positional arguments:
  PATH                  Markdown files or directories to check

options:
  -h, --help            show this help message and exit
  -e, --exclude [ ...]  Files or directories to exclude
  -cm, --check-remote   Check remote references (HTTP/HTTPS links)
  -nc, --no-color        Turn off colored output
  -v, --verbose         Enable verbose output
  --allow-absolute      Allow absolute path references like [ref](/path/to/file.md)
```

<!-- [![codecov](https://codecov.io/gh/flumi3/markdown-refcheck/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/flumi3/markdown-refcheck) -->

## Features

- 🔍 **Reference Detection** - Validate various reference patterns in Markdown files
- ❌ **Broken Link Highlighting** - Quickly identify broken references with clear error messages
- 🌐 **Remote URL Checking** - Validate external HTTP/HTTPS links (optional with `--check-remote`)
- 🛠️ **User-Friendly CLI** - Simple and intuitive command-line interface
- 🎨 **Colored Output** - Clear, color-coded results for easy scanning (disable with `--no-color`)
- ⚙️ **CI/CD Ready** - Perfect for automated quality checks in your documentation workflows
- 🚀 **Pre-commit Integration** - Available as a pre-commit hook
- 💬 **Inline Ignore Comments** - Suppress false positives with [`<!-- refcheck-ignore -->`](docs/Ignoring-References.md) directives

## Installation

RefCheck is available on PyPI:

```bash
pip install refcheck

# or using pipx
pipx install refcheck
```

## Pre-commit Integration

Add this to your `pre-commit-config.yml`:

```yaml
- repo: https://github.com/flumi3/refcheck
  rev: v0.5.0
  hooks:
    - id: refcheck
      args: ["docs/", "--exclude", "docs/filetoexclude.md"]
```

## Examples

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

```text
$ refcheck . --check-remote

[+] Searching for markdown files in C:\Users\flumi3\github\refcheck ...

[+] 2 Markdown files to check.
- tests\sample_markdown.md
- docs\Understanding-Markdown-References.md

[+] FILE: tests\sample_markdown.md...
tests\sample_markdown.md:39: /img/image.png - BROKEN
tests\sample_markdown.md:52: https://www.openai.com/logo.png - BROKEN

[+] FILE: docs\Understanding-Markdown-References.md...
docs\Understanding-Markdown-References.md:42: #local-file-references - OK

Reference check complete.

============================| Summary |=============================
[!] 2 broken references found:
tests\sample_markdown.md:39: /img/image.png
tests\sample_markdown.md:52: https://www.openai.com/logo.png
====================================================================
```

For more advanced configuration options, see the [Integration Guide](docs/Integration-Guide.md).

## Contributing

Contributions are welcome!  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) before opening pull requests.

## Documentation

For more detailed information, check out the documentation:

- [CLI Reference](docs/CLI-Reference.md) - Complete command-line options and usage
- [Ignoring References](docs/Ignoring-References.md) - Suppress false positives with inline comments
- [Integration Guide](docs/Integration-Guide.md) - CI/CD and workflow integration
- [Examples](docs/Examples.md) - Real-world usage examples
