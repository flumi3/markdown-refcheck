"""Tests for refcheck.parsers module."""

import os

from refcheck.parsers import MarkdownParser, Reference, ReferenceMatch


class TestMarkdownParser:
    """Tests for MarkdownParser class."""

    def test_parse_markdown_file_basic_references(self, temp_markdown_file):
        """Test parsing basic markdown references []()."""
        content = """# Test
[link1](file1.md)
[link2](file2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        assert basic_refs[0].link == "file1.md"
        assert basic_refs[0].line_number == 2
        assert basic_refs[1].link == "file2.md"
        assert basic_refs[1].line_number == 3

    def test_parse_markdown_file_basic_images(self, temp_markdown_file):
        """Test parsing image references ![]()."""
        content = """# Test
![alt1](image1.png)
![alt2](image2.jpg)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_images = result["basic_images"]
        assert len(basic_images) == 2
        assert basic_images[0].link == "image1.png"
        assert basic_images[0].line_number == 2
        assert basic_images[1].link == "image2.jpg"
        assert basic_images[1].line_number == 3

    def test_parse_markdown_file_inline_links(self, temp_markdown_file):
        """Test parsing inline links <url>."""
        content = """# Test
Visit <https://example.com> for more.
Email: <user@example.com>
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        inline_links = result["inline_links"]
        assert len(inline_links) == 2
        assert inline_links[0].link == "https://example.com"
        assert inline_links[1].link == "user@example.com"

    def test_parse_markdown_file_code_block_filtering(self, temp_markdown_file):
        """Test that references inside code blocks are ignored."""
        content = """# Test
[real link](real.md)

```markdown
[fake link](fake.md)
```

[another real](real2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        # Should only find the 2 real links, not the one in code block
        assert len(basic_refs) == 2
        assert basic_refs[0].link == "real.md"
        assert basic_refs[1].link == "real2.md"

    def test_parse_markdown_file_inline_code_filtering(self, temp_markdown_file):
        """Test that references inside inline code are ignored."""
        content = """# Test
[real link](real.md)
Inline code: `[fake](fake.md)` should be ignored.
[another real](real2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        assert basic_refs[0].link == "real.md"
        assert basic_refs[1].link == "real2.md"

    def test_parse_markdown_file_mixed_code_filtering(self, temp_markdown_file):
        """Test filtering with both code blocks and inline code."""
        content = """# Test
[real1](real1.md)

```python
# [code block fake](fake1.md)
print("[fake2](fake2.md)")
```

Inline: `[inline fake](fake3.md)`

[real2](real2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        assert basic_refs[0].link == "real1.md"
        assert basic_refs[1].link == "real2.md"

    def test_parse_markdown_file_header_references(self, temp_markdown_file):
        """Test parsing header references."""
        content = """# Test
[same file header](#section-1)
[other file header](other.md#introduction)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        assert basic_refs[0].link == "#section-1"
        assert basic_refs[1].link == "other.md#introduction"

    def test_parse_markdown_file_remote_vs_local(self, temp_markdown_file):
        """Test remote vs local reference classification."""
        content = """# Test
[local](file.md)
[remote](https://example.com)
[http](http://example.org)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 3
        assert basic_refs[0].is_remote is False
        assert basic_refs[1].is_remote is True
        assert basic_refs[2].is_remote is True

    def test_parse_markdown_file_file_not_found(self):
        """Test parsing non-existent file."""
        parser = MarkdownParser()
        result = parser.parse_markdown_file("/nonexistent/file.md")
        assert result == {}

    def test_parse_markdown_file_empty_file(self, temp_markdown_file):
        """Test parsing empty markdown file."""
        file_path = temp_markdown_file("")
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        assert len(result["basic_references"]) == 0
        assert len(result["basic_images"]) == 0
        assert len(result["inline_links"]) == 0

    def test_parse_markdown_file_no_references(self, temp_markdown_file):
        """Test parsing file with no references."""
        content = """# Test
Just plain text without any links.

## Section 2
More text here.
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        assert len(result["basic_references"]) == 0
        assert len(result["basic_images"]) == 0
        assert len(result["inline_links"]) == 0

    def test_parse_markdown_file_line_numbers_accuracy(self, temp_markdown_file):
        """Test that line numbers are accurate."""
        content = """# Line 1
Line 2
[link on line 3](file.md)
Line 4
Line 5
![image on line 6](image.png)
Line 7
<https://example.com>
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        assert result["basic_references"][0].line_number == 3
        assert result["basic_images"][0].line_number == 6
        assert result["inline_links"][0].line_number == 8

    def test_parse_real_fixture_file_code_blocks(self):
        """Test parsing real fixture file with code blocks."""
        fixture_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "code_blocks",
            "code_with_refs.md",
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        basic_refs = result["basic_references"]
        # Should find only real links, not those in code blocks
        real_links = [ref.link for ref in basic_refs]
        assert "real_file.md" in real_links
        assert "another_real.md" in real_links
        assert "final.md" in real_links
        # These should NOT be found (they're in code blocks)
        assert "fake_file.md" not in real_links
        assert "code_ref.md" not in real_links
        assert "nope.md" not in real_links

    def test_parse_real_fixture_file_inline_code(self):
        """Test parsing real fixture file with inline code."""
        fixture_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "code_blocks",
            "inline_code.md",
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        basic_refs = result["basic_references"]
        real_links = [ref.link for ref in basic_refs]
        # Should find real links
        assert "actual_file.md" in real_links
        assert "real.md" in real_links
        # Should NOT find inline code references
        assert "fake.md" not in real_links

    def test_is_remote_reference_http(self):
        """Test remote reference detection for HTTP."""
        parser = MarkdownParser()
        assert parser._is_remote_reference("http://example.com") is True
        assert parser._is_remote_reference("https://example.com") is True

    def test_is_remote_reference_mailto(self):
        """Test remote reference detection for mailto."""
        parser = MarkdownParser()
        assert parser._is_remote_reference("mailto:user@example.com") is True

    def test_is_remote_reference_local_file(self):
        """Test remote reference detection for local files."""
        parser = MarkdownParser()
        assert parser._is_remote_reference("file.md") is False
        assert parser._is_remote_reference("../file.md") is False
        assert parser._is_remote_reference("./file.md") is False
        assert parser._is_remote_reference("/absolute/path.md") is False

    def test_is_remote_reference_header(self):
        """Test remote reference detection for headers."""
        parser = MarkdownParser()
        assert parser._is_remote_reference("#header") is False
        assert parser._is_remote_reference("file.md#header") is False

    def test_drop_code_references_empty_lists(self):
        """Test _drop_code_references with empty input."""
        parser = MarkdownParser()
        result = parser._drop_code_references([], [])
        assert result == []

    def test_drop_code_references_no_code(self):
        """Test _drop_code_references when there are no code sections."""
        parser = MarkdownParser()
        import re

        match = re.search(r"\[(.+?)\]\((.+?)\)", "[link](file.md)")
        ref = ReferenceMatch(line_number=1, match=match)
        result = parser._drop_code_references([ref], [])
        assert len(result) == 1

    def test_process_basic_references(self, temp_markdown_file):
        """Test _process_basic_references method."""
        parser = MarkdownParser()
        content = "[link](file.md)"
        file_path = temp_markdown_file(content)

        import re

        # Use the same pattern as in parsers.py with named groups
        pattern = re.compile(r"!*\[(?P<text>[^\]]+)\]\((?P<link>[^)]+)\)")
        matches = []
        for match in re.finditer(pattern, content):
            matches.append(ReferenceMatch(line_number=1, match=match))

        references = parser._process_basic_references(file_path, matches)
        assert len(references) == 1
        assert references[0].file_path == file_path
        assert references[0].line_number == 1
        assert references[0].link == "file.md"
        assert references[0].syntax == "[link](file.md)"

    def test_find_matches_with_line_numbers(self):
        """Test _find_matches_with_line_numbers method."""
        parser = MarkdownParser()
        import re

        # Use pattern with named groups like in parsers.py
        pattern = re.compile(r"!*\[(?P<text>[^\]]+)\]\((?P<link>[^)]+)\)")
        text = """line 1
[link1](file1.md)
line 3
[link2](file2.md)"""

        matches = parser._find_matches_with_line_numbers(pattern, text)
        assert len(matches) == 2
        assert matches[0].line_number == 2
        assert matches[1].line_number == 4

    def test_parse_multiple_references_same_line(self, temp_markdown_file):
        """Test parsing multiple references on the same line."""
        content = "Here's [link1](file1.md) and [link2](file2.md) on same line."
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        assert basic_refs[0].line_number == basic_refs[1].line_number == 1

    def test_parse_images_not_captured_as_basic_refs(self, temp_markdown_file):
        """Test that images ![]() are not captured as basic references []()."""
        content = """# Test
[link](file.md)
![image](image.png)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        # Basic references should only contain the link, not the image
        basic_refs = result["basic_references"]
        assert len(basic_refs) == 1
        assert basic_refs[0].link == "file.md"

        # Images should be in basic_images
        basic_images = result["basic_images"]
        assert len(basic_images) == 1
        assert basic_images[0].link == "image.png"


class TestReferenceDataClass:
    """Tests for Reference data class."""

    def test_reference_creation(self):
        """Test creating a Reference object."""
        ref = Reference(
            file_path="/path/to/file.md",
            line_number=10,
            syntax="[link](target.md)",
            link="target.md",
            is_remote=False,
        )
        assert ref.file_path == "/path/to/file.md"
        assert ref.line_number == 10
        assert ref.syntax == "[link](target.md)"
        assert ref.link == "target.md"
        assert ref.is_remote is False

    def test_reference_str_representation(self):
        """Test string representation of Reference."""
        ref = Reference(
            file_path="/path/to/file.md",
            line_number=10,
            syntax="[link](target.md)",
            link="target.md",
            is_remote=False,
        )
        str_repr = str(ref)
        assert "Reference:" in str_repr
        assert "/path/to/file.md" in str_repr
        assert "10" in str_repr
        assert "target.md" in str_repr
        assert "Local" in str_repr

    def test_reference_remote_str_representation(self):
        """Test string representation of remote Reference."""
        ref = Reference(
            file_path="/path/to/file.md",
            line_number=5,
            syntax="[link](https://example.com)",
            link="https://example.com",
            is_remote=True,
        )
        str_repr = str(ref)
        assert "Remote" in str_repr
