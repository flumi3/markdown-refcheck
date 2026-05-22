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
        assert len(inline_links) == 1
        assert inline_links[0].link == "https://example.com"

    def test_parse_markdown_file_inline_links_ignores_bare_emails(self, temp_markdown_file):
        """Test that bare emails in angle brackets are not matched as inline links."""
        content = """# Test
Contact <user@example.com> for help.
Or use <mailto:user@example.com> instead.
Visit <https://example.com> for more.
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        inline_links = result["inline_links"]
        assert len(inline_links) == 2
        assert inline_links[0].link == "mailto:user@example.com"
        assert inline_links[1].link == "https://example.com"

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

    def test_parse_markdown_file_html_comment_filtering(self, temp_markdown_file):
        """Test that references inside HTML comments are ignored."""
        content = """# Test
[real link](real.md)
<!-- [commented link](commented.md) -->
[another real](real2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        real_links = [ref.link for ref in basic_refs]
        assert "real.md" in real_links
        assert "real2.md" in real_links
        assert "commented.md" not in real_links

    def test_parse_markdown_file_multiline_html_comment_filtering(self, temp_markdown_file):
        """Test that references inside multi-line HTML comments are ignored."""
        content = """# Test
[real link](real.md)
<!-- This is a markdown comment that spans multiple lines and includes references that should be ignored:
[commented link 1](commented1.md)

[commented link 2](commented2.md)
-->
[another real](real2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 2
        real_links = [ref.link for ref in basic_refs]
        assert "real.md" in real_links
        assert "real2.md" in real_links
        assert "commented1.md" not in real_links
        assert "commented2.md" not in real_links

    def test_parse_markdown_file_html_comment_image_filtering(self, temp_markdown_file):
        """Test that image references inside HTML comments are ignored."""
        content = """# Test
![real image](real.png)
<!-- ![commented image](commented.png) -->
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_images = result["basic_images"]
        assert len(basic_images) == 1
        assert basic_images[0].link == "real.png"

    def test_parse_markdown_file_html_comment_inline_link_filtering(self, temp_markdown_file):
        """Test that inline links inside HTML comments are ignored."""
        content = """# Test
<https://real.com>
<!-- <https://commented.com> -->
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        inline_links = result["inline_links"]
        assert len(inline_links) == 1
        assert inline_links[0].link == "https://real.com"

    def test_parse_markdown_file_duplicate_reference_inside_and_outside_comment(
        self, temp_markdown_file
    ):
        """Test that a reference appearing both inside a comment and outside is still found."""
        content = """# Test
<!-- [dup](same.md) -->
[dup](same.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        basic_refs = result["basic_references"]
        assert len(basic_refs) == 1
        assert basic_refs[0].link == "same.md"
        assert basic_refs[0].line_number == 3


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


class TestRefcheckIgnore:
    """Tests for refcheck-ignore comment directives."""

    def test_standalone_ignore_skips_next_line(self, temp_markdown_file):
        """A standalone <!-- refcheck-ignore --> skips the reference on the next line."""
        content = """\
[kept](kept.md)
<!-- refcheck-ignore -->
[ignored](ignored.md)
[also_kept](also_kept.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md", "also_kept.md"]

    def test_inline_ignore_skips_same_line(self, temp_markdown_file):
        """An inline <!-- refcheck-ignore --> skips the reference on the same line."""
        content = """\
[kept](kept.md)
[ignored](ignored.md) <!-- refcheck-ignore -->
[also_kept](also_kept.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md", "also_kept.md"]

    def test_block_ignore_skips_section(self, temp_markdown_file):
        """References between start/end block directives are skipped."""
        content = """\
[kept_before](before.md)
<!-- refcheck-ignore-start -->
[ignored1](ignored1.md)
[ignored2](ignored2.md)
<!-- refcheck-ignore-end -->
[kept_after](after.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["before.md", "after.md"]

    def test_block_ignore_skips_images(self, temp_markdown_file):
        """Block ignore also skips image references."""
        content = """\
![kept](kept.png)
<!-- refcheck-ignore-start -->
![ignored](ignored.png)
<!-- refcheck-ignore-end -->
![also_kept](also_kept.png)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_images"]]
        assert links == ["kept.png", "also_kept.png"]

    def test_ignore_with_reason(self, temp_markdown_file):
        """Ignore directives with an optional reason are supported."""
        content = """\
[kept](kept.md)
<!-- refcheck-ignore: this is a known false positive -->
[ignored](ignored.md)
[also_kept](also_kept.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md", "also_kept.md"]

    def test_triple_dash_syntax(self, temp_markdown_file):
        """<!--- refcheck-ignore --> with triple-dash is supported."""
        content = """\
[kept](kept.md)
<!--- refcheck-ignore -->
[ignored](ignored.md)
[also_kept](also_kept.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md", "also_kept.md"]

    def test_triple_dash_block_with_reason(self, temp_markdown_file):
        """<!--- refcheck-ignore-start: reason --> with triple-dash and reason."""
        content = """\
[kept](kept.md)
<!--- refcheck-ignore-start: entire section is false positives -->
[ignored1](ignored1.md)
[ignored2](ignored2.md)
<!--- refcheck-ignore-end -->
[also_kept](also_kept.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md", "also_kept.md"]

    def test_ignore_inside_code_block_not_honored(self, temp_markdown_file):
        """Ignore directives inside code blocks should NOT be honored."""
        content = """\
```markdown
<!-- refcheck-ignore -->
[in_code_block](fake.md)
```
[real_link](real.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["real.md"]

    def test_unmatched_block_start_ignores_to_eof(self, temp_markdown_file):
        """An unmatched refcheck-ignore-start ignores references to end of file."""
        content = """\
[kept](kept.md)
<!-- refcheck-ignore-start -->
[ignored1](ignored1.md)
[ignored2](ignored2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md"]

    def test_multiple_ignore_comments(self, temp_markdown_file):
        """Multiple ignore comments in a single file work independently."""
        content = """\
[kept1](kept1.md)
<!-- refcheck-ignore -->
[ignored1](ignored1.md)
[kept2](kept2.md)
<!-- refcheck-ignore -->
[ignored2](ignored2.md)
[kept3](kept3.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept1.md", "kept2.md", "kept3.md"]

    def test_no_over_suppression(self, temp_markdown_file):
        """Inline ignore on line N does not suppress line N+1."""
        content = """\
[ref1](ref1.md) <!-- refcheck-ignore -->
[ref2](ref2.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["ref2.md"]

    def test_fixture_single_line_ignore(self):
        """Test with the single_line_ignore.md fixture file."""
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "ignore_comments", "single_line_ignore.md"
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        links = [r.link for r in result["basic_references"]]
        assert "kept.md" in links
        assert "also_kept.md" in links
        assert "ignored.md" not in links

    def test_fixture_inline_ignore(self):
        """Test with the inline_ignore.md fixture file."""
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "ignore_comments", "inline_ignore.md"
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        links = [r.link for r in result["basic_references"]]
        assert "kept.md" in links
        assert "also_kept.md" in links
        assert "ignored.md" not in links

    def test_fixture_block_ignore(self):
        """Test with the block_ignore.md fixture file."""
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "ignore_comments", "block_ignore.md"
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        links = [r.link for r in result["basic_references"]]
        assert "before.md" in links
        assert "after.md" in links
        assert "ignored1.md" not in links
        assert "ignored2.md" not in links

        img_links = [r.link for r in result["basic_images"]]
        assert "ignored.png" not in img_links

    def test_fixture_ignore_in_code_block(self):
        """Test with the ignore_in_code_block.md fixture file."""
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "ignore_comments", "ignore_in_code_block.md"
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["real.md"]

    def test_fixture_ignore_with_reason(self):
        """Test with the ignore_with_reason.md fixture file."""
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "ignore_comments", "ignore_with_reason.md"
        )
        parser = MarkdownParser()
        result = parser.parse_markdown_file(fixture_path)

        links = [r.link for r in result["basic_references"]]
        assert "kept.md" in links
        assert "also_kept.md" in links
        assert "ignored.md" not in links
        assert "ignored1.md" not in links
        assert "ignored2.md" not in links

    def test_block_end_with_reason(self, temp_markdown_file):
        """Block end directive with an optional reason is recognized."""
        content = """\
[kept](kept.md)
<!-- refcheck-ignore-start: reason -->
[ignored](ignored.md)
<!-- refcheck-ignore-end: done -->
[also_kept](also_kept.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert links == ["kept.md", "also_kept.md"]

    def test_block_markers_do_not_suppress_own_lines(self, temp_markdown_file):
        """References on start/end marker lines are not suppressed."""
        content = """\
[before](before.md) <!-- refcheck-ignore-start -->
[ignored](ignored.md)
<!-- refcheck-ignore-end --> [after](after.md)
"""
        file_path = temp_markdown_file(content)
        parser = MarkdownParser()
        result = parser.parse_markdown_file(file_path)

        links = [r.link for r in result["basic_references"]]
        assert "before.md" in links
        assert "after.md" in links
        assert "ignored.md" not in links
