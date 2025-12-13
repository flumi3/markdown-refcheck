# CHANGELOG


## v0.4.0 (2025-12-13)

### Bug Fixes

- Ensure command line arguments are only parsed when not running under pytest
  ([`b36450b`](https://github.com/flumi3/markdown-refcheck/commit/b36450ba4d3b0f658b854ad2fa42f1528064c8ec))

- Ignore inline code fenced references as they are not real references
  ([`1b7cd7c`](https://github.com/flumi3/markdown-refcheck/commit/1b7cd7cfa3483205f744e3ebec52a322953b7ea3))

- Improve markdown reference validation and parsing
  ([`8f38107`](https://github.com/flumi3/markdown-refcheck/commit/8f38107b5650c4b079ec7ab63e70428e8363461f))

- Optimize regex patterns: replace greedy .+ with specific character classes -
  BASIC_REFERENCE_PATTERN: [^\]]+ for text, [^)]+ for links - INLINE_LINK_PATTERN: [^>]+ instead of
  .+ - Fix _drop_code_block_references: use list filtering instead of modifying during iteration -
  Implement _process_inline_links for processing angle-bracket enclosed links - Activate inline
  links validation in main processing loop - Fix header path resolution: resolve relative markdown
  file paths to absolute before checking for headers (fixes validation of other.md#header patterns)

- Move get_command_line_argumets() from parsers.py to new cli.py to break circular import
  ([`5cb49e7`](https://github.com/flumi3/markdown-refcheck/commit/5cb49e7e33ae95c9b2bf872964f94f4e5d949bb0))

- create new cli.py file and move CLI related code there - update settings.py - update parsers.py

- Outdated lockfile and qa
  ([`bc6ff4a`](https://github.com/flumi3/markdown-refcheck/commit/bc6ff4ac65cd3f772df48b3c228c6d3e07d90b63))

- Qa issues that were only on remote
  ([`146d50f`](https://github.com/flumi3/markdown-refcheck/commit/146d50f9f9d3a63e23f4191ed2ae26e3af7a6f46))

- **cd**: Update build command to ensure poetry is installed before building
  ([`7886095`](https://github.com/flumi3/markdown-refcheck/commit/78860959cc53324b607378a50bba92b020eadc22))

- **ci**: Add contents permission for deploy job
  ([`d66a31f`](https://github.com/flumi3/markdown-refcheck/commit/d66a31f50b1b8c8c7993de12a6936af09ccae9ca))

- **ci**: Comment out code coverage to codecov
  ([`968c632`](https://github.com/flumi3/markdown-refcheck/commit/968c632b995a7b9b0aedbb641f1b52dad1ea97d5))

### Chores

- Make QA happy :)
  ([`53d0a75`](https://github.com/flumi3/markdown-refcheck/commit/53d0a7572b4954fe2b52f4d46eaf054fb8e88305))

- also set line length to 100

- Remove obsolete publish-to-pypi workflow
  ([`5c71104`](https://github.com/flumi3/markdown-refcheck/commit/5c711042d50aeef82f9dfd4e1218116693519576))

- **dependabot**: Configure dependabot to apply security patches
  ([`f471032`](https://github.com/flumi3/markdown-refcheck/commit/f4710328d8a6ac4664184eec389f3d62ec322626))

Add `open-pull-requests-limit: 0`. This will prevent opening of pull requests for normal version
  bumps. Security updates will still be created.

- **deps**: Bump requests from 2.32.3 to 2.32.4
  ([#50](https://github.com/flumi3/markdown-refcheck/pull/50),
  [`d2383f4`](https://github.com/flumi3/markdown-refcheck/commit/d2383f4eafdaadadc1fa3d08b00bc5dde25a2408))

Bumps [requests](https://github.com/psf/requests) from 2.32.3 to 2.32.4. - [Release
  notes](https://github.com/psf/requests/releases) -
  [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md) -
  [Commits](https://github.com/psf/requests/compare/v2.32.3...v2.32.4)

--- updated-dependencies: - dependency-name: requests dependency-version: 2.32.4

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump the pip group with 2 updates
  ([#52](https://github.com/flumi3/markdown-refcheck/pull/52),
  [`185db64`](https://github.com/flumi3/markdown-refcheck/commit/185db642a4202f44c578d6576bbf05ec44e6eb24))

--- updated-dependencies: - dependency-name: requests dependency-version: 2.32.4

dependency-type: direct:production

dependency-group: pip

- dependency-name: urllib3 dependency-version: 2.5.0

dependency-type: indirect

dependency-group: pip ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump urllib3 in the pip group across 1 directory
  ([#80](https://github.com/flumi3/markdown-refcheck/pull/80),
  [`cee5d8b`](https://github.com/flumi3/markdown-refcheck/commit/cee5d8bcc690b35818e224a4f66d92d41760e370))

- **deps-dev**: Bump commitizen from 4.4.1 to 4.6.1
  ([#37](https://github.com/flumi3/markdown-refcheck/pull/37),
  [`ec4822f`](https://github.com/flumi3/markdown-refcheck/commit/ec4822f65f6c4bf52d49cd02db64b28515eef202))

Bumps [commitizen](https://github.com/commitizen-tools/commitizen) from 4.4.1 to 4.6.1. - [Release
  notes](https://github.com/commitizen-tools/commitizen/releases) -
  [Changelog](https://github.com/commitizen-tools/commitizen/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/commitizen-tools/commitizen/compare/v4.4.1...v4.6.1)

--- updated-dependencies: - dependency-name: commitizen dependency-version: 4.6.1

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump commitizen from 4.6.1 to 4.8.3
  ([#49](https://github.com/flumi3/markdown-refcheck/pull/49),
  [`4d114b3`](https://github.com/flumi3/markdown-refcheck/commit/4d114b3eefaaa4487c7c78de26dc7e4b9454caf7))

Bumps [commitizen](https://github.com/commitizen-tools/commitizen) from 4.6.1 to 4.8.3. - [Release
  notes](https://github.com/commitizen-tools/commitizen/releases) -
  [Changelog](https://github.com/commitizen-tools/commitizen/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/commitizen-tools/commitizen/compare/v4.6.1...v4.8.3)

--- updated-dependencies: - dependency-name: commitizen dependency-version: 4.8.3

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.3.5 to 8.4.1
  ([#53](https://github.com/flumi3/markdown-refcheck/pull/53),
  [`c94ac98`](https://github.com/flumi3/markdown-refcheck/commit/c94ac98ec6cd58b100f39516ae0302f8233bd813))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.5 to 8.4.1. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.5...8.4.1)

--- updated-dependencies: - dependency-name: pytest dependency-version: 8.4.1

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.4.1 to 8.4.2
  ([#69](https://github.com/flumi3/markdown-refcheck/pull/69),
  [`ea9d07c`](https://github.com/flumi3/markdown-refcheck/commit/ea9d07cf232644b578fad26a529d512bb46c1e5a))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.4.1 to 8.4.2. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.4.1...8.4.2)

--- updated-dependencies: - dependency-name: pytest dependency-version: 8.4.2

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump python-semantic-release from 10.3.1 to 10.4.1
  ([#73](https://github.com/flumi3/markdown-refcheck/pull/73),
  [`151cf92`](https://github.com/flumi3/markdown-refcheck/commit/151cf929d2f6095bac240c8c5707158b8751a9c6))

Bumps [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 10.3.1 to 10.4.1. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v10.3.1...v10.4.1)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-version: 10.4.1

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump python-semantic-release from 9.21.0 to 9.21.1
  ([#38](https://github.com/flumi3/markdown-refcheck/pull/38),
  [`b2c89f3`](https://github.com/flumi3/markdown-refcheck/commit/b2c89f3e807ad4d3ef80bb6ae1bb1190d76c5299))

Bumps [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.21.0 to 9.21.1. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.21...v9.21.1)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-version: 9.21.1

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump python-semantic-release from 9.21.1 to 10.3.1
  ([#61](https://github.com/flumi3/markdown-refcheck/pull/61),
  [`4da4e26`](https://github.com/flumi3/markdown-refcheck/commit/4da4e265528e7d54ebc6b6328654ef6e96c0f6a2))

Bumps [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.21.1 to 10.3.1. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.21.1...v10.3.1)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-version: 10.3.1

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump ruff from 0.11.2 to 0.11.8
  ([#36](https://github.com/flumi3/markdown-refcheck/pull/36),
  [`a720223`](https://github.com/flumi3/markdown-refcheck/commit/a7202239bbfeedf251066ccd7cbe07cd415ec476))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.11.2 to 0.11.8. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.11.2...0.11.8)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.11.8

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Continuous Integration

- Fix trusted publishing exchange failure
  ([`a8d2ee3`](https://github.com/flumi3/markdown-refcheck/commit/a8d2ee3bc03265aecd12bb66ef166a711e7b4765))

- Update ci workflows to new makefile setup and tools
  ([`c17632c`](https://github.com/flumi3/markdown-refcheck/commit/c17632cd344a487a6323b8671a56445db56bb91b))

### Documentation

- Add CONTRIBUTING.md and enhance documentation
  ([`ba00727`](https://github.com/flumi3/markdown-refcheck/commit/ba00727303d22ac2dc236a312d78cd49079b09ad))

- Document commit conventions and development workflow
  ([`7549cf3`](https://github.com/flumi3/markdown-refcheck/commit/7549cf3d2d6caa506b71cca44da849008fc69f6b))

- Add Commit Convention section explaining conventional commits format - Document which commit types
  trigger version bumps (feat, fix, perf) - Document types that don't trigger releases (docs, chore,
  ci, style, etc.) - Add practical examples of conventional commit messages - Document new version
  management make targets - Add codecov coverage badge to badges section - Remove development status
  notice (preparing for v1.0.0 stable release) - Update development commands documentation

- Fix mistake in pre commit usage example
  ([`43e8dad`](https://github.com/flumi3/markdown-refcheck/commit/43e8dadf766351a4d1dd0a72c947e2d2d8c97a26))

- Improve commit hook example
  ([`ab9e026`](https://github.com/flumi3/markdown-refcheck/commit/ab9e02609b5ab357cdcd1fe687518f6eea811019))

- Update CONTRIBUTING.md with coverage requirements and test instructions and modify README.md for
  Codecov token visibility
  ([`99252b4`](https://github.com/flumi3/markdown-refcheck/commit/99252b4a05f3555beee484ceb53fa4cf3597d75d))

### Features

- Add makefile QA and test setup
  ([`e33ff96`](https://github.com/flumi3/markdown-refcheck/commit/e33ff96156b7ef75e0e28fd2af01bf2cd53faa9f))

- create makefile for running and grouping QA and test commands - add pytest-cov, mypy, vulture, and
  deptry to dev dependencies. - configure vulture with minimum confidence and excluded specific
  patterns. - set up per-rule ignores for deptry. - configure mypy with Python version and warning
  options.

- Add version management commands and pre-commit hook setup
  ([`9536935`](https://github.com/flumi3/markdown-refcheck/commit/95369355da0751e32c4f0a12eb02c66bd57218b6))

- Update make init to auto-install pre-commit hooks - Add make bump-version to preview next version
  - Add make changelog to show unreleased changes - Add make check-version to display current/next
  versions - Add make update-hooks to keep pre-commit hooks current

- Configure commitizen and semantic-release for v1.0.0 transition
  ([`9cd0282`](https://github.com/flumi3/markdown-refcheck/commit/9cd02823a414eed8f7e0cccf59c583ead80e6b2f))

- Add [tool.commitizen] section with version sync and changelog bumping - Update
  [tool.semantic_release] with angular parser and major_on_zero=true - Simplify build_command to use
  'poetry build' directly - Enable Dependabot for pip and github-actions (5 PR limit each) - Create
  .pre-commit-config.yaml with commitizen commit-msg hook - Add pre-commit to dev dependencies

- Modernize CI/CD workflows with Poetry caching and codecov integration
  ([`56bf8fc`](https://github.com/flumi3/markdown-refcheck/commit/56bf8fc0f2999ac98a3ad3435bf650b90db5fc36))

- Replace curl-based Poetry installation with snok/install-poetry@v1 - Enable isolated virtual
  environments (.venv in project root) for caching - Upgrade setup-python from v2/v4 to v5 for
  consistency - Add dependency caching with GitHub Actions cache - Add codecov integration with XML
  coverage reports and artifacts - Fix build-validation.yml matrix strategy with explicit job
  definitions - Add validation for all PR commits using cz check - Create version-preview workflow
  for automatic version bump detection - Remove redundant publish-to-pypi.yml workflow

### Refactoring

- Improve CLI argument parsing exit behavior
  ([`f89c742`](https://github.com/flumi3/markdown-refcheck/commit/f89c742ed39e3304d00040e92659d1570c433534))

- Add sys.exit(0) when no paths provided for cleaner UX - Print help message and exit cleanly
  instead of continuing

- Improve code quality and type safety
  ([`4abcd26`](https://github.com/flumi3/markdown-refcheck/commit/4abcd26f1d9260e74ecbfbbabf7265f69fa07aeb))

- Replace mutable default arguments with None in utils.py: -
  get_markdown_files_from_dir(exclude=None) - get_markdown_files_from_args(exclude=None) - Add
  proper return type hints (list[str]) to: - load_exclusion_patterns() -
  get_markdown_files_from_dir() - get_markdown_files_from_args() - Fix logging configuration to
  preserve error messages in non-verbose mode - Change handler level from CRITICAL to WARNING

### Testing

- Add new test files and expand existing tests
  ([`f914dea`](https://github.com/flumi3/markdown-refcheck/commit/f914dea34798354c6a5b729d2c9a17d1a015e82a))

- **`tests/test_parsers.py`** (27 tests) - Covers `MarkdownParser` class and all parsing methods -
  Tests code block filtering (critical for correctness) - Tests all reference types (basic, images,
  inline links) - Tests edge cases and error handling

- **`tests/test_main.py`** (20 tests) - Covers `ReferenceChecker` class - Covers `main()`
  orchestration function - Tests broken/valid reference detection - Tests remote checking with
  mocked HTTP responses - Tests summary printing and sorting

- **`tests/test_cli.py`** (18 tests) - Covers all CLI arguments and flags - Tests short and long
  flag variants - Tests flag combinations - Tests help/exit behavior

- **`tests/test_settings.py`** (15 tests) - Covers `Settings` class initialization - Tests all
  property accessors - Tests `is_valid()` method - Tests pytest detection logic

- **`tests/test_validators/test_remote_reference.py`** (16 tests) - Covers
  `is_valid_remote_reference()` function - Tests various HTTP status codes - Tests timeout and
  connection errors - Tests SSL certificate errors

- **`tests/test_utils.py`** - Added 7 tests for `load_exclusion_patterns()` - Tests with
  existing/missing `.refcheckignore` - Tests whitespace handling - Tests empty files and comments

- Create test infrastructure
  ([`d80e598`](https://github.com/flumi3/markdown-refcheck/commit/d80e598d09b889dde4d0326ac40646d54587cf55))

- Created `tests/conftest.py` with centralized fixtures: - Settings mocks for all flag combinations
  - HTTP request mocks (success, 404, timeout, SSL errors) - File system helpers (temp files,
  directory structures) - Common test data (sample markdown content)

- Created `tests/fixtures/` directory structure: - `valid/` - Valid markdown with various reference
  types - `code_blocks/` - Code block edge cases - `broken_refs/` - Intentionally broken references
  - `edge_cases/` - Malformed syntax and special characters

- Enhance test coverage configuration and enforce coverage thresholds
  ([`a33f889`](https://github.com/flumi3/markdown-refcheck/commit/a33f889b263eb440ddef3a755de492d2919c3d9b))


## v0.3.0 (2025-03-29)

### Chores

- Enable manual run of workflows
  ([`a52c18b`](https://github.com/flumi3/markdown-refcheck/commit/a52c18b49f5d479291ee5f8c3d8f1a8b1aec4669))

### Continuous Integration

- Add workflow template for pypi publishing
  ([`bf6f404`](https://github.com/flumi3/markdown-refcheck/commit/bf6f4049070e96aec80b1afab320b625192d9a83))

### Documentation

- Add badges
  ([`0ce4e3f`](https://github.com/flumi3/markdown-refcheck/commit/0ce4e3f6256f1228103a19cbe186044d785149db))

- How to publish to pypi with poetry
  ([`ecc1e86`](https://github.com/flumi3/markdown-refcheck/commit/ecc1e86d6211548634207be53c39c40324bf5168))

### Features

- Enable refcheck to be used as pre-commit hook
  ([`39d77ad`](https://github.com/flumi3/markdown-refcheck/commit/39d77adda324e0331c6d5a241158cba1ac846ff5))


## v0.2.0 (2025-03-28)

### Bug Fixes

- Add fetch depth to checkout so semantic release finds tags
  ([`c71804a`](https://github.com/flumi3/markdown-refcheck/commit/c71804a457a02de32c34a0d2dcc81d8f0d8e4013))

- Add write permission
  ([`b44e18b`](https://github.com/flumi3/markdown-refcheck/commit/b44e18ba5f6518f57098b09a4fb2ac42011b719c))

- Attempt to fix warning "no release corresponds" from semantic release
  ([`1a5a9cc`](https://github.com/flumi3/markdown-refcheck/commit/1a5a9cc0e7be7a30498b5a17b4d0a83feda285c2))

- Dependency install with poetry
  ([`afec62b`](https://github.com/flumi3/markdown-refcheck/commit/afec62b7e0b6b3c036addd1e0544b9ec6eddaa2c))

- Use curl for poetry install in ci workflow
  ([`308ec94`](https://github.com/flumi3/markdown-refcheck/commit/308ec94744a7f50161c882b29fa2029b242e2285))

- **cicd**: Take real pypa action version
  ([`6638d3a`](https://github.com/flumi3/markdown-refcheck/commit/6638d3a5a7b0e32679a64fbeb0474f3bc6d6956e))

### Chores

- Add name to build job
  ([`fd6ec59`](https://github.com/flumi3/markdown-refcheck/commit/fd6ec5979b79175424f2e96f687969800d01bede))

- **deps-dev**: Bump commitizen from 4.2.2 to 4.4.1
  ([#22](https://github.com/flumi3/markdown-refcheck/pull/22),
  [`70afcca`](https://github.com/flumi3/markdown-refcheck/commit/70afcca83009ba5fd5dbada14eca8ab476832e97))

Bumps [commitizen](https://github.com/commitizen-tools/commitizen) from 4.2.2 to 4.4.1. - [Release
  notes](https://github.com/commitizen-tools/commitizen/releases) -
  [Changelog](https://github.com/commitizen-tools/commitizen/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/commitizen-tools/commitizen/compare/v4.2.2...v4.4.1)

--- updated-dependencies: - dependency-name: commitizen dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.3.4 to 8.3.5
  ([#23](https://github.com/flumi3/markdown-refcheck/pull/23),
  [`dcd2b38`](https://github.com/flumi3/markdown-refcheck/commit/dcd2b3889137896b292bf04419e0e52a53d9bf19))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.4 to 8.3.5. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.4...8.3.5)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump python-semantic-release from 9.20.0 to 9.21.0
  ([#21](https://github.com/flumi3/markdown-refcheck/pull/21),
  [`f1a3ad7`](https://github.com/flumi3/markdown-refcheck/commit/f1a3ad7452916c490c64c819880de572d6415df8))

Bumps [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.20.0 to 9.21.0. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.20...v9.21)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-type:
  direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump ruff from 0.11.0 to 0.11.2
  ([#27](https://github.com/flumi3/markdown-refcheck/pull/27),
  [`0913ac6`](https://github.com/flumi3/markdown-refcheck/commit/0913ac6ce5892e0c5d4e446d6040a8c38066e87e))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.11.0 to 0.11.2. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.11.0...0.11.2)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump ruff from 0.9.7 to 0.11.0
  ([#26](https://github.com/flumi3/markdown-refcheck/pull/26),
  [`da9f7a3`](https://github.com/flumi3/markdown-refcheck/commit/da9f7a3e3d71bcf078f5b51db42926e2990bc4dc))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.9.7 to 0.11.0. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.9.7...0.11.0)

--- updated-dependencies: - dependency-name: ruff dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Features

- Add semantic release workflow ([#18](https://github.com/flumi3/markdown-refcheck/pull/18),
  [`08dd9a6`](https://github.com/flumi3/markdown-refcheck/commit/08dd9a6d96900ff38f9e17d131bc4b0be90088ef))

* feat: semantic release

* rename ci in hope of that it reflects in github

* fix formatting

- **stdout**: Beautify tool output ([#29](https://github.com/flumi3/markdown-refcheck/pull/29),
  [`3cb53db`](https://github.com/flumi3/markdown-refcheck/commit/3cb53db116ffcdf417de9436ae657c8c7bf170c1))

- replace background color for flagging references BROKEN or OK with normal color to make it look a
  bit calmer - also add skipped references to stdout with a flag SKIPPED and color yellow - add
  colored output for configuration warnings like "remote check will be skipped" - add print
  statement to a checked markdown file saying No references found. if there were no references to
  check, so you don't get the impression something went wrong for that file. - improve print output
  a bit in general

### Refactoring

- Adjust to semantic release removing pypi publishing
  ([`aca8dc5`](https://github.com/flumi3/markdown-refcheck/commit/aca8dc5dd301cdddd4aff5cbf412e39f6d3e4686))

- Ci/cd workflow ([#19](https://github.com/flumi3/markdown-refcheck/pull/19),
  [`6998ef3`](https://github.com/flumi3/markdown-refcheck/commit/6998ef3ef1f5978b371eaa8f361d15e7b908ffbe))

* add workflow template for lint and test

* add build validation workflow

* replace release and ci with ci/cd workflow

* fix: poetry not found

* fix: add code checkout

* fix: seperate job for template use

### Testing

- Add tests for header_exists and is_valid_markdown_reference
  ([#20](https://github.com/flumi3/markdown-refcheck/pull/20),
  [`8e80a13`](https://github.com/flumi3/markdown-refcheck/commit/8e80a1331431a6b96b412544690a5b55afa03695))

* make normalize_header normalize underscores

* add tests for header_exists

* add tests for is_valid_markdown_reference

* add contributing section

* remove unused import


## v0.1.5 (2025-01-22)


## v0.1.4 (2025-01-17)


## v0.1.3 (2024-11-28)

### Refactoring

- Markdown file parsing
  ([`a5625f7`](https://github.com/flumi3/markdown-refcheck/commit/a5625f7965aeb271426aca1374de63d9157abddf))


## v0.1.2 (2024-11-27)

### Bug Fixes

- Release workflow poetry install ([#5](https://github.com/flumi3/markdown-refcheck/pull/5),
  [`e08b80f`](https://github.com/flumi3/markdown-refcheck/commit/e08b80f43035c3d99ec1d31453d96d1e281d535f))

* change workflow name * fix poetry install * add tests to flake8 check and resolve issues

### Features

- Automated dependency updates with Dependabot
  ([#4](https://github.com/flumi3/markdown-refcheck/pull/4),
  [`0fa58ff`](https://github.com/flumi3/markdown-refcheck/commit/0fa58ff14dd9a872eec264554c66c5463d50b021))

- Ci workflow ([#3](https://github.com/flumi3/markdown-refcheck/pull/3),
  [`c28e893`](https://github.com/flumi3/markdown-refcheck/commit/c28e893afc6c0fc4e24212097e1fb5431a3f90e4))

* add flake8 * create ci workflow * change python version to ^3.9

- Directories and paths are now specified together
  ([`a391558`](https://github.com/flumi3/markdown-refcheck/commit/a3915586e4ed50b69ab7fd7e7e3793d21776e7d0))

- remove the -d flag - improve usage output - adjust and improve tests

- Release workflow ([#2](https://github.com/flumi3/markdown-refcheck/pull/2),
  [`09843b6`](https://github.com/flumi3/markdown-refcheck/commit/09843b676316af83ac92e5482b5ecff30864511b))
