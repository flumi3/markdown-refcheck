# Contributing to RefCheck

Contributions are welcome! Please read this guide before opening a pull request.

For detailed setup instructions, architecture, and conventions, see the
[Development Guide](docs/developer-guide/Development-Guide.md).

## Reporting Bugs

Create an issue with: steps to reproduce, expected vs. actual behavior, your environment (OS, Python
version, RefCheck version), and sample Markdown files if applicable.

## Suggesting Features

Check existing issues first, then describe the feature, its benefits, and usage examples.

## Pull Request Workflow

1. Fork the repo and create a branch from `main` (e.g., `feat/add-json-output`,
   `fix/handle-empty-files`)
2. Set up the dev environment: `make init` (see
   [Development Guide](docs/developer-guide/Development-Guide.md#setup))
3. Make your changes and add tests for new functionality
4. Run `make qa` and `make test` — all checks must pass
5. Commit using [conventional commits](#commit-convention)
6. Open a pull request with a clear description

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated
versioning and changelog generation. Pre-commit hooks enforce the format.

```text
<type>(<scope>): <description>
```

**Types that trigger releases:**

| Type                     | Release               |
| ------------------------ | --------------------- |
| `feat:`                  | Minor (0.1.0 → 0.2.0) |
| `fix:`                   | Patch (0.1.0 → 0.1.1) |
| `perf:`                  | Patch                 |
| `BREAKING CHANGE:` / `!` | Major (0.1.0 → 1.0.0) |

**Types that don't trigger releases:** `docs:`, `chore:`, `ci:`, `style:`, `refactor:`, `test:`,
`build:`

**Examples:**

```bash
feat: add support for checking external URL status codes
fix(parser): correctly parse markdown links with special characters
docs: update CLI examples in README
```

## Quality Checklist

Before submitting a PR:

- [ ] All tests pass (`make test`)
- [ ] Code coverage maintained at 80%+ (`make test-coverage`)
- [ ] All quality checks pass (`make qa`)
- [ ] Commit messages follow conventional commits
- [ ] Documentation updated if needed
