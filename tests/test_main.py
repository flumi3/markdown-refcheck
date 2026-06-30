"""Tests for refcheck.main module."""

import pytest
from unittest import mock

from refcheck.main import main, ReferenceChecker, BrokenReference
from refcheck.parsers import Reference


class TestReferenceChecker:
    """Tests for ReferenceChecker class."""

    def test_check_references_local_valid(self, temp_markdown_file, capsys):
        """Test checking valid local references."""
        # Create a real file to reference
        content = "# Test"
        temp_markdown_file(content, "target.md")  # Referenced file
        source_file = temp_markdown_file(content, "source.md")

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](target.md)",
            link="target.md",
            is_remote=False,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = False
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 0

    def test_check_references_local_broken(self, temp_markdown_file, capsys):
        """Test checking broken local references."""
        content = "# Test"
        source_file = temp_markdown_file(content, "source.md")

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](nonexistent.md)",
            link="nonexistent.md",
            is_remote=False,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = False
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 1
        assert checker.broken_references[0].link == "nonexistent.md"

    def test_check_references_remote_skipped(self, temp_markdown_file, capsys):
        """Test that remote references are skipped when check_remote is False."""
        content = "# Test"
        source_file = temp_markdown_file(content)

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](https://example.com)",
            link="https://example.com",
            is_remote=True,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = False
            mock_settings.no_color = True
            checker.check_references([ref])

        # Should not be added to broken_references when skipped
        assert len(checker.broken_references) == 0
        captured = capsys.readouterr()
        assert "SKIPPED" in captured.out

    def test_check_references_remote_valid(self, mock_http_success, temp_markdown_file):
        """Test checking valid remote references."""
        content = "# Test"
        source_file = temp_markdown_file(content)

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](https://example.com)",
            link="https://example.com",
            is_remote=True,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = True
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 0
        mock_http_success.assert_called_once()

    def test_check_references_remote_broken_404(self, mock_http_404, temp_markdown_file):
        """Test checking broken remote references (404)."""
        content = "# Test"
        source_file = temp_markdown_file(content)

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](https://example.com/404)",
            link="https://example.com/404",
            is_remote=True,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = True
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 1
        assert checker.broken_references[0].link == "https://example.com/404"

    def test_check_references_remote_timeout(self, mock_http_timeout, temp_markdown_file):
        """Test checking remote references that timeout."""
        content = "# Test"
        source_file = temp_markdown_file(content)

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](https://slow.example.com)",
            link="https://slow.example.com",
            is_remote=True,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = True
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 1
        assert checker.broken_references[0].link == "https://slow.example.com"

    def test_check_references_markdown_with_header(self, temp_markdown_file):
        """Test checking markdown references with headers."""
        target_content = """# Introduction

## Section A
"""
        source_content = "# Test"
        temp_markdown_file(target_content, "target.md")  # Referenced file
        source_file = temp_markdown_file(source_content, "source.md")

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](target.md#section-a)",
            link="target.md#section-a",
            is_remote=False,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = False
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 0

    def test_check_references_markdown_missing_header(self, temp_markdown_file):
        """Test checking markdown references with missing headers."""
        target_content = """# Introduction

## Section A
"""
        source_content = "# Test"
        temp_markdown_file(target_content, "target.md")  # Referenced file
        source_file = temp_markdown_file(source_content, "source.md")

        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[link](target.md#missing-section)",
            link="target.md#missing-section",
            is_remote=False,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = False
            mock_settings.no_color = True
            checker.check_references([ref])

        assert len(checker.broken_references) == 1

    def test_print_summary_no_broken(self, capsys):
        """Test print_summary with no broken references."""
        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = False
            mock_settings.no_color = True
            checker.print_summary()

        captured = capsys.readouterr()
        assert "No broken references!" in captured.out
        assert "Summary" in captured.out

    def test_print_summary_with_broken(self, temp_markdown_file, capsys):
        """Test print_summary with broken references."""
        content = "# Test"
        source_file = temp_markdown_file(content)

        broken_ref = BrokenReference(
            file_path=source_file,
            line_number=10,
            syntax="[link](missing.md)",
            link="missing.md",
            is_remote=False,
            status="BROKEN",
        )

        checker = ReferenceChecker()
        checker.broken_references = [broken_ref]

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = False
            mock_settings.no_color = True
            checker.print_summary()

        captured = capsys.readouterr()
        assert "1 broken references found" in captured.out
        assert "missing.md" in captured.out

    def test_print_summary_multiple_broken_sorted(self, temp_markdown_file, capsys):
        """Test that broken references are sorted by file and line number."""
        content = "# Test"
        file1 = temp_markdown_file(content, "file1.md")
        file2 = temp_markdown_file(content, "file2.md")

        broken_refs = [
            BrokenReference(
                file_path=file2,
                line_number=5,
                syntax="[link](missing2.md)",
                link="missing2.md",
                is_remote=False,
                status="BROKEN",
            ),
            BrokenReference(
                file_path=file1,
                line_number=10,
                syntax="[link](missing1.md)",
                link="missing1.md",
                is_remote=False,
                status="BROKEN",
            ),
            BrokenReference(
                file_path=file1,
                line_number=5,
                syntax="[link](missing3.md)",
                link="missing3.md",
                is_remote=False,
                status="BROKEN",
            ),
        ]

        checker = ReferenceChecker()
        checker.broken_references = broken_refs

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = False
            mock_settings.no_color = True
            checker.print_summary()

        # After sorting, file1:5 should come before file1:10, and both before file2:5
        assert checker.broken_references[0].file_path == file1
        assert checker.broken_references[0].line_number == 5
        assert checker.broken_references[1].line_number == 10

    def test_print_summary_quiet_no_broken(self, capsys):
        """Test print_summary in quiet mode with no broken references."""
        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = True
            mock_settings.no_color = True
            checker.print_summary()

        captured = capsys.readouterr()
        # In quiet mode, should only show success message, no header/dividers
        assert "No broken references!" in captured.out
        assert "Reference check complete" not in captured.out
        assert "Summary" not in captured.out
        assert "====" not in captured.out

    def test_print_summary_quiet_no_broken_with_color(self, capsys):
        """Test print_summary in quiet mode with no broken refs and color enabled."""
        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = True
            mock_settings.no_color = False
            checker.print_summary()

        captured = capsys.readouterr()
        # Should show emoji success message
        assert "\U0001f389" in captured.out  # Emoji character
        assert "No broken references!" in captured.out
        assert "Reference check complete" not in captured.out

    def test_print_summary_quiet_with_broken(self, temp_markdown_file, capsys):
        """Test print_summary in quiet mode with broken references."""
        content = "# Test"
        source_file = temp_markdown_file(content)

        broken_ref = BrokenReference(
            file_path=source_file,
            line_number=94,
            syntax="[CONTRIBUTING.md](../../CONTRIBUTING.md#commit-convention___)",
            link="../../CONTRIBUTING.md#commit-convention___",
            is_remote=False,
            status="BROKEN",
        )

        checker = ReferenceChecker()
        checker.broken_references = [broken_ref]

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = True
            mock_settings.no_color = True
            checker.print_summary()

        captured = capsys.readouterr()
        # In quiet mode, should show count and per-line format
        assert "[!] 1 broken references found:" in captured.out
        assert (
            f"{source_file}:94: [CONTRIBUTING.md](../../CONTRIBUTING.md#commit-convention___)"
            in captured.out
        )
        # Should NOT show decorative elements
        assert "Reference check complete" not in captured.out
        assert "Summary" not in captured.out
        assert "====" not in captured.out

    def test_print_summary_quiet_multiple_broken_sorted(self, temp_markdown_file, capsys):
        """Test quiet mode with multiple broken refs shows sorted output without decorations."""
        content = "# Test"
        file1 = temp_markdown_file(content, "file1.md")
        file2 = temp_markdown_file(content, "file2.md")

        broken_refs = [
            BrokenReference(
                file_path=file2,
                line_number=5,
                syntax="[link](missing2.md)",
                link="missing2.md",
                is_remote=False,
                status="BROKEN",
            ),
            BrokenReference(
                file_path=file1,
                line_number=10,
                syntax="[link](missing1.md)",
                link="missing1.md",
                is_remote=False,
                status="BROKEN",
            ),
            BrokenReference(
                file_path=file1,
                line_number=5,
                syntax="[link](missing3.md)",
                link="missing3.md",
                is_remote=False,
                status="BROKEN",
            ),
        ]

        checker = ReferenceChecker()
        checker.broken_references = broken_refs

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.quiet = True
            mock_settings.no_color = True
            checker.print_summary()

        captured = capsys.readouterr()
        # Verify count header
        assert "[!] 3 broken references found:" in captured.out
        # Verify all refs are present
        assert "missing1.md" in captured.out
        assert "missing2.md" in captured.out
        assert "missing3.md" in captured.out
        # Verify sorting (file1:5 before file1:10 before file2:5)
        output_lines = captured.out.split("\n")
        file1_line5_idx = None
        file1_line10_idx = None
        file2_line5_idx = None
        for idx, line in enumerate(output_lines):
            if f"{file1}:5:" in line:
                file1_line5_idx = idx
            elif f"{file1}:10:" in line:
                file1_line10_idx = idx
            elif f"{file2}:5:" in line:
                file2_line5_idx = idx

        assert file1_line5_idx is not None
        assert file1_line10_idx is not None
        assert file2_line5_idx is not None
        assert file1_line5_idx < file1_line10_idx < file2_line5_idx
        # Verify no decorations
        assert "Reference check complete" not in captured.out


class TestMainFunction:
    """Tests for main() function."""

    def test_main_no_files_found(self, capsys):
        """Test main when no markdown files are found."""
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = ["/nonexistent"]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[]):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "No Markdown files specified or found" in captured.out

    def test_main_invalid_settings(self):
        """Test main with invalid settings."""
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.is_valid.return_value = False

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    def test_main_single_file_no_references(self, temp_markdown_file, capsys):
        """Test main with a single file containing no references."""
        content = "# Test\n\nJust plain text."
        test_file = temp_markdown_file(content)

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [test_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[test_file]):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "No broken references!" in captured.out

    def test_main_file_with_valid_references(self, temp_markdown_file, capsys):
        """Test main with files containing valid references."""
        target_content = "# Target"
        source_content = "[link](target.md)"

        temp_markdown_file(target_content, "target.md")  # Referenced file
        source_file = temp_markdown_file(source_content, "source.md")

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [source_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch(
                "refcheck.main.get_markdown_files_from_args", return_value=[source_file]
            ):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "No broken references!" in captured.out

    def test_main_file_with_broken_references(self, temp_markdown_file, capsys):
        """Test main with files containing broken references."""
        content = "[broken link](nonexistent.md)"
        test_file = temp_markdown_file(content)

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [test_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[test_file]):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "1 broken references found" in captured.out
        assert "nonexistent.md" in captured.out

    def test_main_check_remote_warning(self, temp_markdown_file, capsys):
        """Test that warning is displayed when remote checking is disabled."""
        content = "# Test"
        test_file = temp_markdown_file(content)

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [test_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[test_file]):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Skipping remote reference check" in captured.out

    def test_main_verbose_logging(self, temp_markdown_file):
        """Test that verbose logging is configured correctly."""
        content = "# Test"
        test_file = temp_markdown_file(content)

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [test_file]
            mock_settings.exclude = []
            mock_settings.verbose = True
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[test_file]):
                with mock.patch("refcheck.main.setup_logging") as mock_setup_logging:
                    with pytest.raises(SystemExit) as exc_info:
                        main()

            assert exc_info.value.code == 0
            mock_setup_logging.assert_called_once_with(verbose=True)

    def test_main_multiple_files(self, temp_markdown_file, capsys):
        """Test main with multiple markdown files."""
        file1 = temp_markdown_file("# File 1", "file1.md")
        file2 = temp_markdown_file("# File 2", "file2.md")

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [file1, file2]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            with mock.patch(
                "refcheck.main.get_markdown_files_from_args", return_value=[file1, file2]
            ):
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "2 Markdown files to check" in captured.out

    def test_main_reconfigures_stdout_to_utf8(self, temp_markdown_file):
        """Test that main() reconfigures stdout/stderr to UTF-8 to avoid UnicodeEncodeError
        on Windows consoles that use a narrow encoding such as cp1252."""
        content = "# Test"
        test_file = temp_markdown_file(content)

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [test_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            mock_stdout = mock.MagicMock()
            mock_stderr = mock.MagicMock()

            with (
                mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[test_file]),
                mock.patch("sys.stdout", mock_stdout),
                mock.patch("sys.stderr", mock_stderr),
            ):
                with pytest.raises(SystemExit):
                    main()

        mock_stdout.reconfigure.assert_called_once_with(encoding="utf-8", errors="backslashreplace")
        mock_stderr.reconfigure.assert_called_once_with(encoding="utf-8", errors="backslashreplace")

    def test_main_reconfigure_skipped_when_not_available(self, temp_markdown_file):
        """Test that main() does not crash when stdout/stderr lack a reconfigure method
        (e.g. when output is redirected to a file or a legacy stream)."""
        content = "# Test"
        test_file = temp_markdown_file(content)

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [test_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.is_valid.return_value = True

            # Simulate a stream that does not expose reconfigure (e.g. a plain BytesIO wrapper).
            class _NoReconfigure:
                def write(self, s):
                    pass

                def flush(self):
                    pass

            with (
                mock.patch("refcheck.main.get_markdown_files_from_args", return_value=[test_file]),
                mock.patch("sys.stdout", _NoReconfigure()),
                mock.patch("sys.stderr", _NoReconfigure()),
            ):
                # Should not raise AttributeError or any other exception.
                with pytest.raises(SystemExit):
                    main()


class TestUnicodeHandling:
    """Tests that Unicode characters in reference syntax are handled without errors."""

    def test_check_references_unicode_syntax_no_error(self, temp_markdown_file, capsys):
        """Regression test: references whose syntax contains characters outside cp1252
        (e.g. the arrow '→' / U+2192) must not raise UnicodeEncodeError when printed."""
        content = "# Test"
        source_file = temp_markdown_file(content, "source.md")
        temp_markdown_file(content, "target.md")

        # Simulate a link text that contains a non-cp1252 character (→).
        ref = Reference(
            file_path=source_file,
            line_number=1,
            syntax="[Step A → Step B](target.md)",
            link="target.md",
            is_remote=False,
        )

        checker = ReferenceChecker()
        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.check_remote = False
            mock_settings.no_color = True
            # Must not raise any exception.
            checker.check_references([ref])

        captured = capsys.readouterr()
        assert "→" in captured.out
        assert len(checker.broken_references) == 0

    def test_main_with_cp1252_stdout_does_not_raise(self, temp_markdown_file):
        """Behavioral regression for the Windows cp1252 UnicodeEncodeError.

        Patches sys.stdout with a real TextIOWrapper that starts with cp1252 encoding
        (mimicking a Windows console) and verifies that main() reconfigures it to UTF-8
        so that reference syntax containing '→' (U+2192) is printed without crashing.
        """
        import io

        source_content = "[Step A → Step B](target.md)"
        temp_markdown_file("# Target", "target.md")
        source_file = temp_markdown_file(source_content, "source.md")

        # Build a cp1252-encoded stdout that mirrors a Windows narrow-encoding console.
        stdout_buf = io.BytesIO()
        narrow_stdout = io.TextIOWrapper(stdout_buf, encoding="cp1252")
        stderr_buf = io.BytesIO()
        narrow_stderr = io.TextIOWrapper(stderr_buf, encoding="cp1252")

        with mock.patch("refcheck.main.settings") as mock_settings:
            mock_settings.paths = [source_file]
            mock_settings.exclude = []
            mock_settings.verbose = False
            mock_settings.check_remote = False
            mock_settings.no_color = True
            mock_settings.quiet = False
            mock_settings.is_valid.return_value = True

            with (
                mock.patch(
                    "refcheck.main.get_markdown_files_from_args", return_value=[source_file]
                ),
                mock.patch("sys.stdout", narrow_stdout),
                mock.patch("sys.stderr", narrow_stderr),
            ):
                # Without the fix this would raise UnicodeEncodeError because '→' cannot
                # be encoded in cp1252.  With the fix, main() reconfigures stdout to UTF-8
                # before any printing occurs.
                with pytest.raises(SystemExit) as exc_info:
                    main()

        assert exc_info.value.code == 0

        narrow_stdout.flush()
        output = stdout_buf.getvalue().decode("utf-8")
        assert "→" in output


class TestBrokenReferenceDataClass:
    """Tests for BrokenReference data class."""

    def test_broken_reference_creation(self):
        """Test creating a BrokenReference object."""
        broken_ref = BrokenReference(
            file_path="/path/to/file.md",
            line_number=10,
            syntax="[link](broken.md)",
            link="broken.md",
            is_remote=False,
            status="BROKEN",
        )

        assert broken_ref.file_path == "/path/to/file.md"
        assert broken_ref.line_number == 10
        assert broken_ref.link == "broken.md"
        assert broken_ref.status == "BROKEN"
