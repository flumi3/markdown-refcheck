# Ignoring References

RefCheck supports HTML comment directives to suppress reference checking on specific lines or sections. This is useful
for handling false positives or references that are intentionally broken (e.g., placeholder links, VPN-only URLs).

## Table of Contents

- [Skip a Single Line](#skip-a-single-line)
- [Skip a Section](#skip-a-section)
- [Optional Reason](#optional-reason)
- [Syntax Details](#syntax-details)

## Skip a Single Line

Place the comment on its own line to skip the reference on the **next** line:

```markdown
<!-- refcheck-ignore -->
[This reference will not be checked](./some/path.md)
```

Or place it inline to skip the reference on the **same** line:

```markdown
[This reference will not be checked](./some/path.md) <!-- refcheck-ignore -->
```

## Skip a Section

Wrap a block of lines with start/end directives to skip all references within:

```markdown
<!-- refcheck-ignore-start -->
[ignored](./a.md)
[also ignored](./b.md)
<!-- refcheck-ignore-end -->
```

References before and after the block are still checked as normal.

## Optional Reason

All directives accept an optional reason after a colon. This is purely for documentation purposes and does not affect
behavior:

```markdown
<!-- refcheck-ignore: external link only available on VPN -->
[internal docs](https://internal.example.com/docs)

<!-- refcheck-ignore-start: placeholder links for upcoming feature -->
[feature docs](./upcoming/feature.md)
[feature API](./upcoming/api.md)
<!-- refcheck-ignore-end: placeholder links for upcoming feature -->
```

## Syntax Details

- Both `<!--` and `<!---` (triple-dash) syntax are supported.
- Directives inside fenced code blocks (` ``` `) or inline code (`` ` ``) are **not** honored.
- Block start/end markers should be placed on their own lines.
- All reference types are affected: basic references, images, and inline links.
