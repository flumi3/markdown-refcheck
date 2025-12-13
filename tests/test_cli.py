"""Tests for refcheck.cli module."""

import pytest
import sys
from unittest import mock

from refcheck.cli import get_command_line_arguments


class TestGetCommandLineArguments:
    """Tests for get_command_line_arguments function."""

    def test_cli_single_file(self):
        """Test CLI with a single file."""
        test_args = ["refcheck", "file.md"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.paths == ["file.md"]
            assert args.exclude == []
            assert args.check_remote is False
            assert args.no_color is False
            assert args.verbose is False
            assert args.allow_absolute is False

    def test_cli_multiple_files(self):
        """Test CLI with multiple files."""
        test_args = ["refcheck", "file1.md", "file2.md", "file3.md"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.paths == ["file1.md", "file2.md", "file3.md"]

    def test_cli_directory(self):
        """Test CLI with a directory."""
        test_args = ["refcheck", "docs/"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.paths == ["docs/"]

    def test_cli_exclude_files(self):
        """Test CLI with --exclude flag."""
        test_args = ["refcheck", "docs/", "--exclude", "node_modules", ".git"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.paths == ["docs/"]
            assert args.exclude == ["node_modules", ".git"]

    def test_cli_exclude_short_flag(self):
        """Test CLI with -e (short exclude flag)."""
        test_args = ["refcheck", "docs/", "-e", "node_modules"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.exclude == ["node_modules"]

    def test_cli_check_remote_flag(self):
        """Test CLI with --check-remote flag."""
        test_args = ["refcheck", "file.md", "--check-remote"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.check_remote is True

    def test_cli_check_remote_short_flag(self):
        """Test CLI with -cm (short check-remote flag)."""
        test_args = ["refcheck", "file.md", "-cm"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.check_remote is True

    def test_cli_no_color_flag(self):
        """Test CLI with --no-color flag."""
        test_args = ["refcheck", "file.md", "--no-color"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.no_color is True

    def test_cli_no_color_short_flag(self):
        """Test CLI with -nc (short no-color flag)."""
        test_args = ["refcheck", "file.md", "-nc"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.no_color is True

    def test_cli_verbose_flag(self):
        """Test CLI with --verbose flag."""
        test_args = ["refcheck", "file.md", "--verbose"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.verbose is True

    def test_cli_verbose_short_flag(self):
        """Test CLI with -v (short verbose flag)."""
        test_args = ["refcheck", "file.md", "-v"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.verbose is True

    def test_cli_allow_absolute_flag(self):
        """Test CLI with --allow-absolute flag."""
        test_args = ["refcheck", "file.md", "--allow-absolute"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.allow_absolute is True

    def test_cli_all_flags_combined(self):
        """Test CLI with all flags combined."""
        test_args = [
            "refcheck",
            "file1.md",
            "file2.md",
            "--exclude",
            "node_modules",
            "--check-remote",
            "--no-color",
            "--verbose",
            "--allow-absolute",
        ]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.paths == ["file1.md", "file2.md"]
            assert args.exclude == ["node_modules"]
            assert args.check_remote is True
            assert args.no_color is True
            assert args.verbose is True
            assert args.allow_absolute is True

    def test_cli_no_paths_exits(self):
        """Test that CLI exits when no paths are provided."""
        test_args = ["refcheck"]
        with mock.patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                get_command_line_arguments()
            assert exc_info.value.code == 0

    def test_cli_mixed_files_and_directories(self):
        """Test CLI with both files and directories."""
        test_args = ["refcheck", "README.md", "docs/", "guides/"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.paths == ["README.md", "docs/", "guides/"]

    def test_cli_exclude_multiple_patterns(self):
        """Test CLI with multiple exclude patterns."""
        test_args = [
            "refcheck",
            ".",
            "-e",
            "node_modules",
            ".git",
            "build",
            "dist",
        ]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.exclude == ["node_modules", ".git", "build", "dist"]

    def test_cli_paths_attribute_type(self):
        """Test that paths attribute is always a list."""
        test_args = ["refcheck", "file.md"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert isinstance(args.paths, list)

    def test_cli_exclude_default_empty_list(self):
        """Test that exclude defaults to empty list when not provided."""
        test_args = ["refcheck", "file.md"]
        with mock.patch.object(sys, "argv", test_args):
            args = get_command_line_arguments()
            assert args.exclude == []
            assert isinstance(args.exclude, list)
