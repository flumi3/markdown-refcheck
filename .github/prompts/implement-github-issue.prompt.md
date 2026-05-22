---
description:
  "Full issue-to-PR workflow: fetch issue, analyse, plan, branch, implement, test, and open PR"
argument-hint: "Issue number, e.g. 42"
agent: "agent"
tools: [vscode, execute, read, agent, edit, search, web, browser, "github/*", todo]
---

# Implement GitHub Issue

You are implementing a GitHub issue end-to-end for this repository. Issue number provided by the
user: **$input**

Follow every step in order. Do not skip steps.

---

## Step 1 — Fetch & Analyse the Issue

Use the `github-issue` skill to retrieve full details for issue **$input**:

- Title, description, acceptance criteria, labels, comments
- Any linked issues or PRs

After fetching, critically evaluate the issue:

- Is the description still accurate given the current codebase?
- Are the acceptance criteria clear and achievable?
- Are there any ambiguities or conflicts with existing architecture?
- Are there any things to assess before creating an implementation plan?
- Are there any concerns about the implementation that should be resolved before starting?

Document your findings as a short analysis before proceeding.

---

## Step 2 — Gather Codebase Context

Explore the repository to understand what is relevant to this issue:

- Identify affected files, modules, and layers (API, domain, DB, frontend)
- Read existing code that will be modified or extended
- Check for related tests, migrations, and documentation
- Consult
  [docs/architecture/project-architecture-blueprint.md](../architecture/project-architecture-blueprint.md)
  and any relevant ADRs in [docs/adr/](../adr/) if architectural decisions are involved

Only gather context that is directly relevant — do not read the entire codebase.

---

## Step 3 — Create an Actionable Plan

Before writing any code, **use the Plan agent in a subagent** to create an implementation plan.
Review the created plan carefully. If it needs adjustments, provide feedback to the Plan agent and
iterate until you have a clear, actionable plan. If anything is unclear, resolve it now by reading
more code or conducting research. If really necessary, ask the user for clarification.

---

## Step 4 — Prepare the Branch

Ensure the local repo is on an up-to-date `main`, then create a new branch:

```bash
git fetch origin main:main
git checkout -b <type>/$input-<short-descriptive-slug> main
```

Branch prefix rules (pick one based on issue labels):

- `feature/` — new feature or enhancement
- `fix/` — bug fix
- `chore/` — maintenance, dependency update, refactor, documentation
- `test/` — test coverage only
- `ci/` — CI/CD pipeline changes
- `docs/` — documentation changes

The short slug should be 2-5 lowercase words separated by hyphens, summarising the issue.

---

## Step 5 — Implement the Changes

Work through the plan from Step 3. Follow all project conventions.

- Make commits as logical, standalone units of work (not one giant commit)
- Commit message format: `<type>(<scope>): <imperative summary>` (e.g.
  `feat(api): add symbol filter endpoint`)
- Do not add unnecessary comments, docstrings, or abstractions beyond what the issue requires

---

## Step 6 — Quality Checks & Tests

Run the applicable QA pipeline. Only skip a check if it is **provably irrelevant** to the changes
made.

**Code changes:**

```bash
make qa        # format, lint, type-check, dead-code, unused-deps
make test      # unit + integration + e2e
```

**Documentation changes:**

```bash
make docs-qa          # check for broken links, formatting issues, etc.
```

Fix every error or warning before continuing. Do not suppress linters or type checkers without a
documented reason.

---

## Step 7 — Self-Review

Before opening a PR, review your own changes critically:

- Use a subagent with fresh context to review the changes using the Reviewer agent.
- Assess the code review provided by the subagent and implement necessary steps to address the
  findings.
- If you made changes based on the review, run the quality checks and tests again to ensure
  everything still passes.
- After addressing the review feedback, prompt the subagent to confirm that all issues have been
  resolved satisfactorily.

## Step 8 — Verify Acceptance Criteria

Go back to the acceptance criteria gathered in Step 1 and confirm each one is met:

- [ ] Tick off each criterion explicitly
- [ ] If any criterion cannot be met, document why and what was done instead

---

## Step 9 — Open a Pull Request

Using a subagent with GitHub MCP tools, create a pull request on `flumi3/trading-edge` from the
current branch into `main`.

Fill in [.github/PULL_REQUEST_TEMPLATE.md](../PULL_REQUEST_TEMPLATE.md) completely:

- **Summary**: one or two sentences describing the change; include `Closes #$input`
- **Type of change**: tick all that apply
- **Changes**: bullet list of key changes with brief reasoning
- **How to test**: concrete steps a reviewer can follow to verify the PR

PR title format: `<type>: <imperative summary> (#$input)`

Set labels that match the issue labels where applicable.
