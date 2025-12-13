# Code Blocks with References

This file tests that references inside code blocks are ignored.

This is a real [link](real_file.md).

```markdown
This is a fake [link](fake_file.md) inside a code block. ![Fake image](fake.png)
```

This is another real [link](another_real.md).

```python
# Comment with [reference](code_ref.md)
url = "https://example.com"
print("[Not a real link](nope.md)")
```

Inline code should also be ignored: `[fake](inline.md)`.

But this [real link](final.md) should be detected.

## Nested Code

```javascript
const markdown = `
This is nested markdown in code: [nested](nested.md)
`;
```

## HTML in Code

```html
<a href="html_link.md">HTML Link</a> <img src="html_image.png" alt="HTML Image" />
```
