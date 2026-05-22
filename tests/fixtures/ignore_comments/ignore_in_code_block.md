# Ignore In Code Block Test

Directives inside code blocks should NOT be honored.

```markdown
<!-- refcheck-ignore -->
[should_be_filtered_by_code_block](fake.md)
```

[real_link](real.md)
