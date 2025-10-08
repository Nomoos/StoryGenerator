"""Tests for string_utils module.

Demonstrates TDD best practices in Python:
- Red-Green-Refactor cycle
- Parameterized tests with pytest
- Type hints
- Clear test names
- Arrange-Act-Assert pattern
"""

import pytest
from src.Python.utils.string_utils import truncate_with_ellipsis


class TestTruncateWithEllipsis:
    """Test suite for truncate_with_ellipsis function."""

    @pytest.mark.parametrize(
        "text,max_length,expected",
        [
            ("Hello World", 20, "Hello World"),
            ("Short", 100, "Short"),
            ("Exactly twenty c", 16, "Exactly twenty c"),
            ("", 10, ""),
        ],
    )
    def test_text_shorter_or_equal_to_max_length_returns_original(
        self, text: str, max_length: int, expected: str
    ) -> None:
        """Test that text shorter than or equal to max_length is returned unchanged."""
        # Act
        result = truncate_with_ellipsis(text, max_length)

        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "text,max_length,expected",
        [
            ("This is a very long text that needs to be truncated", 20, "This is a very lo..."),
            ("Another long text for testing purposes", 15, "Another long..."),
            ("Short text but needs truncation", 10, "Short t..."),
        ],
    )
    def test_text_longer_than_max_length_returns_truncated_with_ellipsis(
        self, text: str, max_length: int, expected: str
    ) -> None:
        """Test that text longer than max_length is truncated with ellipsis."""
        # Act
        result = truncate_with_ellipsis(text, max_length)

        # Assert
        assert result == expected
        assert len(result) == max_length

    def test_none_text_raises_type_error(self) -> None:
        """Test that None text raises TypeError."""
        # Act & Assert
        with pytest.raises(TypeError, match="text must be a string"):
            truncate_with_ellipsis(None, 10)  # type: ignore

    @pytest.mark.parametrize("max_length", [0, -1, -10])
    def test_invalid_max_length_raises_value_error(self, max_length: int) -> None:
        """Test that invalid max_length raises ValueError."""
        # Arrange
        text = "Test text"

        # Act & Assert
        with pytest.raises(ValueError, match="max_length must be greater than 0"):
            truncate_with_ellipsis(text, max_length)

    def test_non_string_text_raises_type_error(self) -> None:
        """Test that non-string text raises TypeError."""
        # Act & Assert
        with pytest.raises(TypeError, match="text must be a string"):
            truncate_with_ellipsis(123, 10)  # type: ignore

    def test_unicode_text_handled_correctly(self) -> None:
        """Test that unicode characters are handled correctly."""
        # Arrange
        text = "Hello 世界! This is a test with emojis 🎉🎊"
        max_length = 20

        # Act
        result = truncate_with_ellipsis(text, max_length)

        # Assert
        assert len(result) == max_length
        assert result.endswith("...")
