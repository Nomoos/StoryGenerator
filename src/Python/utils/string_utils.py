"""String utilities for text processing.

TDD example demonstrating Red-Green-Refactor cycle in Python.
"""

from typing import Optional


def truncate_with_ellipsis(text: str, max_length: int) -> str:
    """Truncate text to maximum length, adding ellipsis if needed.

    Args:
        text: The text to truncate.
        max_length: Maximum length of the result.

    Returns:
        Truncated text with ellipsis if needed, or original text if shorter.

    Raises:
        ValueError: If max_length is less than or equal to 0.
        TypeError: If text is not a string.

    Examples:
        >>> truncate_with_ellipsis("Hello World", 20)
        'Hello World'
        >>> truncate_with_ellipsis("This is a very long text", 15)
        'This is a ve...'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if max_length <= 0:
        raise ValueError("max_length must be greater than 0")

    if len(text) <= max_length:
        return text

    ellipsis = "..."
    truncate_length = max_length - len(ellipsis)
    return text[:truncate_length] + ellipsis
