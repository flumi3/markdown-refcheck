import re
import logging
from re import Pattern, Match
from dataclasses import dataclass

logger = logging.getLogger()

CODE_BLOCK_PATTERN = re.compile(r"```(?P<content>[\s\S]*?)```")
INLINE_CODE_PATTERN = re.compile(r"`(?P<content>[^`\n]+)`")
HTML_COMMENT_PATTERN = re.compile(r"<!--(?P<content>[\s\S]*?)-->")

# Refcheck ignore directives — support both <!-- and <!--- (2 or 3 dashes)
REFCHECK_IGNORE_PATTERN = re.compile(r"<!---?\s*refcheck-ignore\s*(?::.*?)?\s*-->")
REFCHECK_IGNORE_START_PATTERN = re.compile(r"<!---?\s*refcheck-ignore-start\s*(?::.*?)?\s*-->")
REFCHECK_IGNORE_END_PATTERN = re.compile(r"<!---?\s*refcheck-ignore-end\s*(?::.*?)?\s*-->")


# Basic Markdown references
BASIC_REFERENCE_PATTERN = re.compile(r"!*\[(?P<text>[^\]]+)\]\((?P<link>[^)]+)\)")  # []() and ![]()
BASIC_IMAGE_PATTERN = re.compile(r"!\[(?P<text>[^(){}\[\]]+)\]\((?P<link>[^(){}\[\]]+)\)")  # ![]()

# Inline Links - <http://example.com>
INLINE_LINK_PATTERN = re.compile(r"<(?P<link>(?:https?://|mailto:)[^>]+)>")

RAW_LINK_PATTERN = re.compile(
    r"(^| )(?:(https?://\S+))"
)  # all links that are surrounded by nothing or spaces
HTML_LINK_PATTERN = re.compile(
    r"<a\s+(?:[^>]*?\s+)?href=([\"\'])(.*?)\1"
)  # <a href="http://example.com">

# Local File References - scripts, markdown files, and local images
HTML_IMAGE_PATTERN = re.compile(
    r"<img\s+(?:[^>]*?\s+)?src=([\"\'])(.*?)\1"
)  # <img src="image.png">


@dataclass
class Reference:
    """Data class to store reference information.

    Attributes:
        file_path: Path to the file where the reference was found.
        line_number: Line number where the reference was found.
        syntax: Syntax of the reference, e.g. `[text](link)`.
        link: The link part of the reference, e.g. `link` in `[text](link)`.
        is_remote: Whether the reference is a remote reference.
    """

    file_path: str
    line_number: int
    syntax: str
    link: str
    is_remote: bool

    def __str__(self):
        """Return a user-friendly string representation of the Reference."""
        remote_status = "Remote" if self.is_remote else "Local"
        return (
            f"Reference:\n"
            f"  File Path: {self.file_path}\n"
            f"  Line Number: {self.line_number}\n"
            f"  Syntax: {self.syntax}\n"
            f"  Link: {self.link}\n"
            f"  Status: {remote_status}"
        )


@dataclass
class ReferenceMatch:
    line_number: int
    match: Match


class MarkdownParser:
    def parse_markdown_file(self, file_path: str) -> dict[str, list[Reference]]:
        """Parse a markdown file to extract references.

        Args:
            file_path: Path to the markdown file.

        Returns:
            A dictionary containing lists of references found in the markdown file.
        """
        logger.info(f"Parsing markdown file: '{file_path}' ...")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return {}
        except IOError as e:
            print(f"Error: An I/O error occurred while reading the file {file_path}: {e}")
            return {}

        # Get all code blocks, such as ```python ... ```, or ```text``` for ensuring that found references are not part
        # of code blocks.
        logger.info("Extracting code blocks ...")
        code_blocks = self._find_matches_with_line_numbers(CODE_BLOCK_PATTERN, content)
        logger.info(f"Found {len(code_blocks)} code blocks.")

        # Get all inline code spans with backticks
        logger.info("Extracting inline code ...")
        inline_code = self._find_matches_with_line_numbers(INLINE_CODE_PATTERN, content)
        logger.info(f"Found {len(inline_code)} inline code spans.")

        # Get all HTML comments, such as <!-- ... -->
        logger.info("Extracting HTML comments ...")
        html_comments = self._find_matches_with_line_numbers(HTML_COMMENT_PATTERN, content)
        logger.info(f"Found {len(html_comments)} HTML comments.")

        # Combine code blocks, inline code, and HTML comments for filtering
        all_code = code_blocks + inline_code + html_comments

        # Determine which lines should be ignored via refcheck-ignore directives.
        # Only filter against code blocks and inline code (not HTML comments), since
        # refcheck-ignore directives are themselves HTML comments.
        logger.info("Checking for refcheck-ignore directives ...")
        ignored_lines = self._get_ignored_lines(content, code_blocks + inline_code)

        # Get all references that look like this: [text](reference)
        logger.info("Extracting basic references ...")
        basic_reference_matches = self._find_matches_with_line_numbers(
            BASIC_REFERENCE_PATTERN, content
        )
        basic_reference_matches = [
            ref for ref in basic_reference_matches if not ref.match[0].startswith("!")
        ]
        logger.info(f"Found {len(basic_reference_matches)} basic reference matches:")
        for ref_match in basic_reference_matches:
            logger.info(ref_match.__repr__())

        basic_reference_matches = self._drop_code_references(basic_reference_matches, all_code)
        basic_reference_matches = self._drop_ignored_references(
            basic_reference_matches, ignored_lines
        )
        logger.info("Processing reference matches...")
        basic_references = self._process_basic_references(file_path, basic_reference_matches)

        # Get all image references that look like this: ![text](reference)
        logger.info("Extracting basic images ...")
        basic_image_matches = self._find_matches_with_line_numbers(BASIC_IMAGE_PATTERN, content)
        logger.info(f"Found {len(basic_image_matches)} basic images.")
        basic_image_matches = self._drop_code_references(basic_image_matches, all_code)
        basic_image_matches = self._drop_ignored_references(basic_image_matches, ignored_lines)
        basic_images = self._process_basic_references(file_path, basic_image_matches)

        logger.info("Extracting inline links ...")
        inline_link_matches = self._find_matches_with_line_numbers(INLINE_LINK_PATTERN, content)
        logger.info(f"Found {len(inline_link_matches)} inline links.")
        inline_link_matches = self._drop_code_references(inline_link_matches, all_code)
        inline_link_matches = self._drop_ignored_references(inline_link_matches, ignored_lines)
        inline_links = self._process_basic_references(file_path, inline_link_matches)

        return {
            "basic_references": basic_references,
            "basic_images": basic_images,
            "inline_links": inline_links,
        }

    def _drop_code_references(
        self, references: list[ReferenceMatch], code_sections: list[ReferenceMatch]
    ) -> list[ReferenceMatch]:
        """Drop references that are part of code blocks, inline code, or HTML comments."""
        logger.info(
            "Dropping references that are part of code blocks, inline code, or HTML comments ..."
        )

        # Filter out references whose source span is contained within a code/comment section span.
        # Position-based comparison prevents incorrectly dropping references that share the same
        # text as a commented-out or code-block reference but appear at a different location.
        filtered_references = []
        dropped_counter = 0

        for ref in references:
            is_in_filtered_section = False
            for section in code_sections:
                if section.match.start(0) <= ref.match.start(0) and ref.match.end(
                    0
                ) <= section.match.end(0):
                    logger.info(f"Dropping reference: {ref.match.group(0)}")
                    is_in_filtered_section = True
                    dropped_counter += 1
                    break

            if not is_in_filtered_section:
                filtered_references.append(ref)

        if dropped_counter > 0:
            logger.info(f"Dropped {dropped_counter} references.")
        else:
            logger.info("No filtered references found.")

        return filtered_references

    def _is_remote_reference(self, link: str) -> bool:
        """Check if a link is a remote reference."""
        protocol_pattern = re.compile(
            r"^([a-zA-Z][a-zA-Z\d+\-.]*):.*"
        )  # matches anything that looks like a `protocol:`
        return bool(protocol_pattern.match(link))

    def _process_basic_references(
        self, file_path: str, matches: list[ReferenceMatch]
    ) -> list[Reference]:
        """Process basic references."""
        references: list[Reference] = []
        for match in matches:
            link = match.match.group("link")
            reference = Reference(
                file_path=file_path,
                line_number=match.line_number,
                syntax=match.match.group(0),
                link=link,
                is_remote=self._is_remote_reference(link),
            )
            references.append(reference)
        return references

    def _process_inline_links(
        self, file_path: str, matches: list[ReferenceMatch]
    ) -> list[Reference]:
        """Process inline links enclosed in angle brackets.

        Handles patterns like:
        - <http://example.com>
        - <a href="https://www.example.org">Example</a>
        - <img src="https://example.com/image.png" alt="Image">
        """
        references: list[Reference] = []
        for match in matches:
            link = match.match.group("link")
            reference = Reference(
                file_path=file_path,
                line_number=match.line_number,
                syntax=match.match.group(0),
                link=link,
                is_remote=self._is_remote_reference(link),
            )
            references.append(reference)
        return references

    def _get_ignored_lines(self, content: str, code_sections: list[ReferenceMatch]) -> set[int]:
        """Determine which lines should be ignored based on refcheck-ignore directives.

        Supports:
        - Single-line: ``<!-- refcheck-ignore -->`` (standalone → next line, inline → same line)
        - Block: ``<!-- refcheck-ignore-start -->`` ... ``<!-- refcheck-ignore-end -->``
        """
        ignored_lines: set[int] = set()

        # --- Single-line ignore directives ---
        ignore_matches = self._find_matches_with_line_numbers(REFCHECK_IGNORE_PATTERN, content)
        # Exclude single-line directives that also match the start/end patterns
        ignore_matches = [
            m
            for m in ignore_matches
            if not REFCHECK_IGNORE_START_PATTERN.match(m.match.group(0))
            and not REFCHECK_IGNORE_END_PATTERN.match(m.match.group(0))
        ]
        ignore_matches = self._drop_code_references(ignore_matches, code_sections)

        for m in ignore_matches:
            if self._is_standalone_comment(m.match, content):
                ignored_lines.add(m.line_number + 1)
            else:
                ignored_lines.add(m.line_number)

        # --- Block ignore directives ---
        start_matches = self._find_matches_with_line_numbers(REFCHECK_IGNORE_START_PATTERN, content)
        start_matches = self._drop_code_references(start_matches, code_sections)

        end_matches = self._find_matches_with_line_numbers(REFCHECK_IGNORE_END_PATTERN, content)
        end_matches = self._drop_code_references(end_matches, code_sections)

        total_lines = content.count("\n") + 1

        for start in start_matches:
            # Find the first end directive that comes after this start directive
            matching_end = None
            for end in end_matches:
                if end.line_number > start.line_number:
                    matching_end = end
                    break

            if matching_end:
                for line in range(start.line_number + 1, matching_end.line_number):
                    ignored_lines.add(line)
            else:
                logger.info(
                    f"Unmatched refcheck-ignore-start at line {start.line_number}, "
                    f"ignoring references until end of file."
                )
                for line in range(start.line_number + 1, total_lines + 1):
                    ignored_lines.add(line)

        if ignored_lines:
            logger.info(f"Ignoring references on lines: {sorted(ignored_lines)}")

        return ignored_lines

    def _is_standalone_comment(self, match: Match, content: str) -> bool:
        """Check if a comment is the only non-whitespace content on its line."""
        # Find the start of the line containing this match
        line_start = content.rfind("\n", 0, match.start(0)) + 1
        # Find the end of the line containing this match
        line_end = content.find("\n", match.end(0))
        if line_end == -1:
            line_end = len(content)

        before = content[line_start : match.start(0)]
        after = content[match.end(0) : line_end]
        return before.strip() == "" and after.strip() == ""

    def _drop_ignored_references(
        self, references: list[ReferenceMatch], ignored_lines: set[int]
    ) -> list[ReferenceMatch]:
        """Drop references that are on ignored lines."""
        if not ignored_lines:
            return references

        filtered = []
        dropped_counter = 0

        for ref in references:
            if ref.line_number in ignored_lines:
                logger.info(f"Dropping ignored reference: {ref.match.group(0)}")
                dropped_counter += 1
            else:
                filtered.append(ref)

        if dropped_counter > 0:
            logger.info(f"Dropped {dropped_counter} ignored references.")

        return filtered

    def _find_matches_with_line_numbers(
        self, pattern: Pattern[str], text: str
    ) -> list[ReferenceMatch]:
        """Find regex matches along with their line numbers."""
        matches_with_line_numbers = []
        for match in re.finditer(pattern, text):
            start_pos = match.start(0)
            line_number = text.count("\n", 0, start_pos) + 1
            matches_with_line_numbers.append(ReferenceMatch(line_number=line_number, match=match))
        return matches_with_line_numbers
