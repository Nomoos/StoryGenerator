#!/usr/bin/env python3
"""
Test demonstrating pytest fixtures usage.

This example shows how to use fixtures from conftest.py
to write cleaner, more maintainable tests.
"""

import json
import pytest
from pathlib import Path


class TestFixtureUsage:
    """Demonstrate using shared fixtures from conftest.py."""

    def test_temp_dir_fixture(self, temp_dir):
        """Test that temp_dir fixture provides a working directory."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()

        # Create a file in the temp directory
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, World!")

        assert test_file.exists()
        assert test_file.read_text() == "Hello, World!"

    def test_sample_json_file_fixture(self, sample_json_file):
        """Test that sample_json_file fixture provides valid JSON."""
        assert sample_json_file.exists()

        # Read and parse the JSON
        with open(sample_json_file) as f:
            data = json.load(f)

        assert data["test"] == "value"
        assert data["number"] == 42
        assert data["array"] == [1, 2, 3]

    def test_sample_text_file_fixture(self, sample_text_file):
        """Test that sample_text_file fixture provides valid text."""
        assert sample_text_file.exists()

        content = sample_text_file.read_text()
        assert "sample" in content
        assert len(content) > 0

    def test_mock_environment_variables(self, mock_environment_variables):
        """Test that environment variables are mocked correctly."""
        import os

        assert os.getenv("TEST_VAR") == "test_value"
        assert os.getenv("DEBUG") == "true"
        assert "TEST_VAR" in mock_environment_variables


@pytest.fixture
def calculator():
    """Local fixture for Calculator instance."""

    class Calculator:
        def add(self, a: int, b: int) -> int:
            return a + b

    return Calculator()


class TestLocalFixtures:
    """Demonstrate local fixtures defined in the test file."""

    def test_with_local_fixture(self, calculator):
        """Test using a fixture defined in this file."""
        result = calculator.add(2, 3)
        assert result == 5


class TestMarkers:
    """Demonstrate pytest markers for test categorization."""

    @pytest.mark.unit
    def test_unit_example(self):
        """A simple unit test."""
        assert 1 + 1 == 2

    @pytest.mark.slow
    def test_slow_operation(self):
        """A test marked as slow (won't run with 'pytest -m "not slow"')."""
        import time

        time.sleep(0.1)  # Simulate slow operation
        assert True

    @pytest.mark.integration
    def test_integration_example(self, temp_dir):
        """An integration test that uses file system."""
        file_path = temp_dir / "integration_test.txt"
        file_path.write_text("integration data")
        assert file_path.read_text() == "integration data"


class TestParametrizedWithFixtures:
    """Demonstrate combining parameterized tests with fixtures."""

    @pytest.mark.parametrize(
        "content,expected_length",
        [
            ("short", 5),
            ("medium text", 11),
            ("a much longer piece of text", 27),
        ],
    )
    def test_file_content_length(self, temp_dir, content, expected_length):
        """Test file operations with different content lengths."""
        file_path = temp_dir / "test.txt"
        file_path.write_text(content)

        actual_content = file_path.read_text()
        assert len(actual_content) == expected_length


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
