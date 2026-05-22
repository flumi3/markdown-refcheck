---
name: github-issue
description: >
  GitHub issue management for trading-edge. Always use this skill when: creating a new issue,
  updating an existing issue, looking up issues, linking/referencing issues, or triaging and
  assigning priorities. Enforces issue templates (.github/ISSUE_TEMPLATE/) and the priority + label
  taxonomy defined below. DO NOT USE FOR: PR reviews (use code-review skill); debugging CI (use
  github-actions-debugging skill).
---

# GitHub Issue Management

Manages GitHub issues for the `flumi3/trading-edge` repository: creation, updates, lookups, and
cross-referencing. Every issue **must** have exactly one priority label. All other labels are
additive.

---

## Label Taxonomy

### Priority labels (exactly one required per issue)

| Label | Meaning                                                        | Examples                                               |
| ----- | -------------------------------------------------------------- | ------------------------------------------------------ |
| `P0`  | Critical / production-blocking. Needs immediate attention.     | Data loss, security vuln, complete feature outage      |
| `P1`  | High. Significantly impacts usability or development velocity. | Major bug, missing core feature blocking a sprint goal |
| `P2`  | Medium. Important but not urgent. Normal backlog.              | Incremental improvements, non-blocking bugs            |
| `P3`  | Low. Nice-to-have / future consideration.                      | Minor polish, exploratory refactors, tech-debt cleanup |

> **Priority assessment guide**: Ask — _"What is the blast radius if this is not addressed in the
> next sprint?"_
>
> - System down / data corruption → **P0**
> - Major workflow blocked → **P1**
> - Degraded but workable → **P2**
> - No immediate impact → **P3**

### Categorisation labels (add all that apply)

| Label              | When to use                                                                           |
| ------------------ | ------------------------------------------------------------------------------------- |
| `frontend`         | Affects React/TypeScript/Vite frontend code                                           |
| `backend`          | Affects FastAPI/Python backend code                                                   |
| `bug`              | Something is broken or behaving unexpectedly (always paired with Bug Report template) |
| `dependencies`     | Dependency updates or version conflicts                                               |
| `documentation`    | Docs additions or corrections                                                         |
| `duplicate`        | Already tracked in another issue (close and link the original)                        |
| `enhancement`      | New capability or improvement (always paired with Feature Request template)           |
| `good first issue` | Low complexity; suitable entry point for new contributors                             |
| `help wanted`      | Input or assistance from others is needed                                             |
| `invalid`          | Not a real issue / not reproducible                                                   |
| `javascript`       | JS-specific concern (use alongside `frontend`)                                        |
| `python:uv`        | Python packaging / uv-specific concern                                                |
| `question`         | Clarification or discussion needed, not necessarily actionable                        |
| `refactor`         | Code restructuring without behaviour change                                           |
| `technical-debt`   | Known suboptimal design that needs addressing later                                   |
| `testing`          | Test coverage, test infrastructure, or flaky tests                                    |
| `wontfix`          | Acknowledged but intentionally not addressed                                          |

---

## Issue Templates

Three templates live in `.github/ISSUE_TEMPLATE/`. Always match the issue type to the correct
template.

| Template file        | Use when                                                                                              | Default label                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `bug_report.md`      | Something is broken or behaving unexpectedly                                                          | `bug`                                           |
| `feature_request.md` | New capability or improvement to existing behaviour                                                   | `enhancement`                                   |
| `task.md`            | Defined unit of work that is neither a bug nor a feature (refactor, config change, dependency update) | _(none — pick the most fitting category label)_ |

---

## Workflows

If possible delegate the following workflows to a subagent.

### 1 — Create a New Issue

**Step 1: Classify** Determine which template fits:

- Unexpected / broken behaviour → `bug_report.md`
- New functionality / improvement → `feature_request.md`
- Defined work (refactor, chore, dependency bump) → `task.md`

**Step 2: Assess priority** Apply the priority assessment guide above. If the user has not specified
a priority, ask one clarifying question: _"What is the impact if this is not fixed/done this
sprint?"_ and map the answer.

**Step 3: Select additional labels** Pick all labels that apply from the categorisation table. At
minimum add `backend` or `frontend` (or both) when the scope is clear.

**Step 4: Draft the issue body** Fill in every section of the chosen template. Do not leave
placeholder comments in the final body — either populate them or remove the section.

**Step 5: Create the issue** Use the `mcp_github_issue_write` tool with:

```json
{
  "owner": "flumi3",
  "repo": "trading-edge",
  "title": "<concise, action-oriented title>",
  "body": "<filled template>",
  "labels": ["<priority>", "<category>", ...]
}
```

**Step 6: Confirm** Report the created issue number and URL, and echo the labels applied.

---

### 2 — Update an Existing Issue

**Step 1: Look up the issue** If only a title or keyword is known, use `mcp_github_search_issues` to
find it. If the number is known, use `mcp_github_issue_read`.

**Step 2: Determine what changes** Common update scenarios:

- Re-prioritise: swap priority label (remove old P-label, add new one)
- Add context: append to the body (do not overwrite — preserve history)
- Change status: add `wontfix`, `duplicate`, etc.
- Link related issues: add a **Related Issues** section (see §4)

**Step 3: Apply changes** Use `mcp_github_issue_write` with `issue_number` to update title, body, or
labels.

---

### 3 — Look Up Issues

Search patterns:

| Goal             | Tool + query                                                     |
| ---------------- | ---------------------------------------------------------------- |
| Find by keyword  | `mcp_github_search_issues`: `repo:flumi3/trading-edge <keyword>` |
| List by label    | `mcp_github_list_issues` with `labels` filter                    |
| Find by priority | `mcp_github_list_issues` with `labels: ["P0"]` (or P1/P2/P3)     |
| Find open bugs   | `mcp_github_list_issues` with `labels: ["bug"]`, `state: "open"` |

Always display results as a markdown table: `#number | title | labels | state`.

---

### 4 — Reference / Link Issues

When an issue relates to, blocks, or is blocked by another issue, add a **Related Issues** section
at the bottom of the body using GitHub's linking keywords:

```markdown
## Related Issues

- Blocks #<number> — <one-line reason>
- Blocked by #<number> — <one-line reason>
- Related to #<number> — <one-line reason>
- Duplicate of #<number>
```

GitHub automatically creates a cross-reference when these are saved. After updating, add a short
comment on the _referenced_ issue as well so both sides are aware, using
`mcp_github_add_issue_comment`.

---

## Quality Checklist

Before finalising any create or update operation, verify:

- [ ] Exactly one priority label (`P0`–`P3`) is assigned
- [ ] Template structure is complete (no unfilled placeholder comments)
- [ ] At least one categorisation label is assigned
- [ ] Title is action-oriented and ≤ 72 characters
- [ ] For bugs: Steps to Reproduce are concrete and reproducible
- [ ] For features: Acceptance Criteria use checkboxes
- [ ] For tasks: Work to be done uses checkboxes
- [ ] Related issues are linked where known
