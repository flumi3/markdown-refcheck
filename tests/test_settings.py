"""Tests for refcheck.settings module."""

import pytest
import sys
from unittest import mock

from refcheck.settings import Settings


class TestSettings:
    """Tests for Settings class."""

    def test_settings_initialization_with_pytest(self):
        """Test that settings returns empty defaults when running under pytest."""
        # This test runs under pytest, so it should get empty defaults
        settings = Settings()
        assert settings.paths == []
        assert settings.verbose is False
        assert settings.check_remote is False
        assert settings.no_color is False
        assert settings.allow_absolute is False
        assert settings.exclude == []

    def test_settings_initialization_without_pytest(self):
        """Test settings initialization when not running under pytest."""
        # Temporarily remove pytest from sys.modules
        pytest_module = sys.modules.get("pytest")
        if pytest_module:
            del sys.modules["pytest"]

        try:
            # Mock the CLI arguments
            mock_args = mock.Mock()
            mock_args.paths = ["file.md"]
            mock_args.verbose = True
            mock_args.check_remote = True
            mock_args.no_color = True
            mock_args.allow_absolute = True
            mock_args.exclude = ["node_modules"]

            with mock.patch("refcheck.settings.get_command_line_arguments", return_value=mock_args):
                settings = Settings()
                assert settings.paths == ["file.md"]
                assert settings.verbose is True
                assert settings.check_remote is True
                assert settings.no_color is True
                assert settings.allow_absolute is True
                assert settings.exclude == ["node_modules"]
        finally:
            # Restore pytest module
            if pytest_module:
                sys.modules["pytest"] = pytest_module

    def test_settings_paths_property(self):
        """Test paths property."""
        settings = Settings()
        assert isinstance(settings.paths, list)

    def test_settings_verbose_property(self):
        """Test verbose property."""
        settings = Settings()
        assert isinstance(settings.verbose, bool)

    def test_settings_check_remote_property(self):
        """Test check_remote property."""
        settings = Settings()
        assert isinstance(settings.check_remote, bool)

    def test_settings_no_color_property(self):
        """Test no_color property."""
        settings = Settings()
        assert isinstance(settings.no_color, bool)

    def test_settings_allow_absolute_property(self):
        """Test allow_absolute property."""
        settings = Settings()
        assert isinstance(settings.allow_absolute, bool)

    def test_settings_exclude_property(self):
        """Test exclude property."""
        settings = Settings()
        assert isinstance(settings.exclude, list)

    def test_settings_str_representation(self):
        """Test __str__ method."""
        settings = Settings()
        str_repr = str(settings)
        assert "Settings(" in str_repr
        assert "paths=" in str_repr
        assert "verbose=" in str_repr
        assert "check_remote=" in str_repr
        assert "no_color=" in str_repr
        assert "allow_absolute=" in str_repr
        assert "exclude=" in str_repr

    def test_settings_is_valid_with_paths(self):
        """Test is_valid returns True when paths are provided."""
        pytest_module = sys.modules.get("pytest")
        if pytest_module:
            del sys.modules["pytest"]

        try:
            mock_args = mock.Mock()
            mock_args.paths = ["file.md"]
            mock_args.verbose = False
            mock_args.check_remote = False
            mock_args.no_color = False
            mock_args.allow_absolute = False
            mock_args.exclude = []

            with mock.patch("refcheck.settings.get_command_line_arguments", return_value=mock_args):
                settings = Settings()
                assert settings.is_valid() is True
        finally:
            if pytest_module:
                sys.modules["pytest"] = pytest_module

    def test_settings_is_valid_without_paths(self):
        """Test is_valid returns False when paths are empty."""
        settings = Settings()
        # Under pytest, paths are empty by default
        assert settings.is_valid() is False

    def test_settings_is_valid_with_empty_list(self):
        """Test is_valid returns False when paths is an empty list."""
        pytest_module = sys.modules.get("pytest")
        if pytest_module:
            del sys.modules["pytest"]

        try:
            mock_args = mock.Mock()
            mock_args.paths = []
            mock_args.verbose = False
            mock_args.check_remote = False
            mock_args.no_color = False
            mock_args.allow_absolute = False
            mock_args.exclude = []

            with mock.patch("refcheck.settings.get_command_line_arguments", return_value=mock_args):
                settings = Settings()
                assert settings.is_valid() is False
        finally:
            if pytest_module:
                sys.modules["pytest"] = pytest_module

    def test_settings_properties_are_read_only(self):
        """Test that properties don't have setters (read-only)."""
        settings = Settings()
        # Attempting to set a property should raise AttributeError
        with pytest.raises(AttributeError):
            settings.paths = ["new_file.md"]

    def test_settings_multiple_paths(self):
        """Test settings with multiple paths."""
        pytest_module = sys.modules.get("pytest")
        if pytest_module:
            del sys.modules["pytest"]

        try:
            mock_args = mock.Mock()
            mock_args.paths = ["file1.md", "file2.md", "docs/"]
            mock_args.verbose = False
            mock_args.check_remote = False
            mock_args.no_color = False
            mock_args.allow_absolute = False
            mock_args.exclude = []

            with mock.patch("refcheck.settings.get_command_line_arguments", return_value=mock_args):
                settings = Settings()
                assert len(settings.paths) == 3
                assert "file1.md" in settings.paths
                assert "file2.md" in settings.paths
                assert "docs/" in settings.paths
        finally:
            if pytest_module:
                sys.modules["pytest"] = pytest_module

    def test_settings_multiple_exclude_patterns(self):
        """Test settings with multiple exclude patterns."""
        pytest_module = sys.modules.get("pytest")
        if pytest_module:
            del sys.modules["pytest"]

        try:
            mock_args = mock.Mock()
            mock_args.paths = ["docs/"]
            mock_args.verbose = False
            mock_args.check_remote = False
            mock_args.no_color = False
            mock_args.allow_absolute = False
            mock_args.exclude = ["node_modules", ".git", "build"]

            with mock.patch("refcheck.settings.get_command_line_arguments", return_value=mock_args):
                settings = Settings()
                assert len(settings.exclude) == 3
                assert "node_modules" in settings.exclude
                assert ".git" in settings.exclude
                assert "build" in settings.exclude
        finally:
            if pytest_module:
                sys.modules["pytest"] = pytest_module
