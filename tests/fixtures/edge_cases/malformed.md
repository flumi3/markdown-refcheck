# Malformed Markdown Test

Testing edge cases and malformed syntax.

## Incomplete References

Missing closing bracket: [incomplete link](file.md

Missing parenthesis: [link]file.md)

Empty reference: [](empty.md)

Empty text: [text]()

## Nested Brackets

Nested: [[double brackets]](file.md)

Multiple: [[[triple]]](file.md)

## Mixed Formats

HTML and Markdown: <a href="mixed.md">[link](text.md)</a>

## Whitespace

Link with [multiple spaces](file.md)

Link with [newline](file.md)

## Escaped Characters

Escaped bracket: \[not a link\](file.md)

Escaped parenthesis: [link]\(file.md\)
