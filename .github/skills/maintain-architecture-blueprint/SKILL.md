---
name: maintain-architecture-blueprint
description: >
  Audits the project-architecture-blueprint.md against the current codebase, identifies drifts
  (incorrect info), gaps (missing info), and outdated sections, then proposes and applies a targeted
  set of updates. USE FOR: keeping the blueprint accurate after code changes; running a periodic
  blueprint health-check; verifying a PR didn't silently break blueprint accuracy. DO NOT USE FOR:
  generating the blueprint from scratch (use `architecture-blueprint-generator`). applyTo:
  "docs/architecture/project-architecture-blueprint.md"
---

# Maintain Architecture Blueprint Skill

## Purpose

Keep `docs/architecture/project-architecture-blueprint.md` accurate and up-to-date by comparing the
living codebase against the document and patching divergences. The workflow always follows **Analyze
→ Plan → Execute** — never edit the document blindly.

---

## Step 0 — Locate the Blueprint

Read `docs/architecture/project-architecture-blueprint.md` in full before doing anything else. Note
the current **Date** and **Version** in the header.

---

## Step 1 — Codebase Snapshot (Probe Phase)

Gather a fresh inventory of the areas most at risk of drift. Run parallel searches covering all of
the major sections in the blueprint. Specifically verify:

| Area               | What to check                                                                        |
| ------------------ | ------------------------------------------------------------------------------------ |
| **Enums**          | `backend/app/domain/models/enums.py` — every enum class and its string VALUES        |
| **Domain config**  | `backend/app/domain/config/*.py` — all Pydantic fields + types + defaults            |
| **Strategies**     | `backend/app/domain/strategies/` — concrete strategy class names, config fields      |
| **DB models**      | `backend/app/db/models/*.py` — SQLAlchemy column names and types                     |
| **Repositories**   | `backend/app/db/repositories/*.py` — every public `async def` method signature       |
| **Services**       | `backend/app/services/**/*.py` — class names, public method signatures               |
| **API routes**     | `backend/app/api/routes/*.py` — `@router.get/post/delete` paths and `response_model` |
| **Alembic**        | `backend/alembic/versions/` — list all migration files                               |
| **Frontend stack** | `frontend/package.json` — dependency names and versions                              |
| **Frontend tree**  | `frontend/src/` — directory tree (especially new pages/hooks/utils)                  |
| **ADRs**           | `docs/adr/` — list all files; check for new ones not already in the blueprint        |
| **Settings**       | `backend/app/config/settings.py` — all Settings fields                               |

Use `grep`, `sed`, or the Explore sub-agent for efficiency. Do **not** guess — read actual source.

---

## Step 2 — Drift Analysis (Compare Phase)

For each blueprint section, compare what the document says against what the code actually contains.
Record every discrepancy under one of three categories:

### Drift Taxonomy

| Category          | Definition                                                 | Examples                                                                   |
| ----------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Factual error** | Document states something that is currently wrong          | Wrong endpoint path, missing/extra enum members, incorrect field name      |
| **Gap**           | Information exists in code but is absent from the document | New fields on a config model, missing repository method, undocumented enum |
| **Stale**         | Information was once true but no longer matches            | Renamed method, removed feature, version number                            |

> **Severity guide:** Factual errors are Critical; gaps in public APIs are High; gaps in
> internal/private details are Medium; cosmetic / wording issues are Low.

---

## Step 3 — Change Plan (Proposal Phase)

Before touching the document, produce a Markdown table listing every change:

```markdown
| #   | Section | Drift Category | Current (wrong)                 | Correct (new)                     | Severity |
| --- | ------- | -------------- | ------------------------------- | --------------------------------- | -------- |
| 1   | §8.1    | Factual error  | `GET /ohlcv`                    | `GET /{base}/{quote}/{timeframe}` | Critical |
| 2   | §5.5    | Gap            | RejectionReason shows 3 members | All 10 members with string values | High     |
```

Present this table to the user and wait for confirmation **if any change is Critical** or if there
are more than 10 changes. For routine maintenance (all Medium/Low), proceed directly.

---

## Step 4 — Execute Changes

Apply all approved changes using `multi_replace_string_in_file` for maximum efficiency:

1. **Header**: Bump `**Date:**` to today's date and increment `**Version:**` by 0.1.
2. **Section-by-section**: Apply changes in document order to avoid context confusion.
3. **Verification**: After editing, `grep` for the key updated strings to confirm each change landed
   correctly.

### Change application rules

- **Factual errors** — replace incorrect text with correct text; keep surrounding prose intact.
- **Gaps (new content)** — add the missing information in the most natural position within the
  existing section. Do not create new top-level sections for minor additions.
- **Stale content** — update in-place; add a one-line note if the old behaviour is worth remembering
  (e.g., "formerly `CompletedTrade`").
- **Never rewrite entire sections** — surgical edits only. Preserve existing prose, diagrams, and
  Mermaid blocks unless they are themselves incorrect.

---

## Step 5 — Quality Check

After all edits run a final verification:

```text
✓ All Critical and High drifts resolved
✓ Header Date and Version updated
✓ No new broken links introduced (check internal anchors if section headers changed)
✓ grep for key updated strings confirms changes are present
✓ Document still renders as valid Markdown (no unclosed code fences, broken tables)
```

---

## Decision Points

| Situation                                                            | Action                                                                                                       |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Migration files added but no new DB models                           | Document the new migration in §6.4 table only                                                                |
| New strategy added                                                   | Add to §5.1 with config field table                                                                          |
| Endpoint path changed                                                | Update §8.1 route table AND §11.3 data pipeline if affected                                                  |
| New ADR created                                                      | Append row to §17 ADR summary table                                                                          |
| Major new subsystem or layer added                                   | Flag for the `architecture-blueprint-generator` skill — full-section rewrites are outside this skill's scope |
| Drift is ambiguous (can't determine correct value from source alone) | Create a GitHub issue describing a follow up investigation using the github tool.                            |

---

## Example Prompts

```
Maintain the project-architecture-blueprint.md file — check it for any drifts, gaps, or outdated information and update it.
```

```
We just added a new strategy. Update the architecture blueprint.
```

```
I added two new Alembic migrations and renamed a repository method. Audit and patch the blueprint.
```

---

## Related Skills / Customizations

- **`architecture-blueprint-generator`** — generate a blueprint from scratch when none exists or a
  full rewrite is needed.
- **`db-schema-diagram`** — update `docs/architecture/db/database-schema.mermaid` after migrations;
  run alongside this skill when DB models change.
