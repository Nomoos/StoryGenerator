"""User profile models demonstrating immutable dataclasses.

TDD example showcasing Python best practices:
- Frozen dataclasses for immutability
- Type hints
- Validation in __post_init__
- Clear documentation
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class UserProfile:
    """Immutable user profile with validation.

    This demonstrates Step 3 of Python best practices: using frozen dataclasses
    for value objects and DTOs to ensure immutability.

    Attributes:
        username: Unique username for the user.
        email: User's email address.
        full_name: User's full name.
        created_at: Timestamp of profile creation.
        bio: Optional biography text.
    """

    username: str
    email: str
    full_name: str
    created_at: datetime
    bio: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate profile data after initialization.

        Raises:
            ValueError: If any validation fails.
        """
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")

        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")

        if not self.full_name:
            raise ValueError("Full name is required")

    def get_display_name(self) -> str:
        """Get the display name for the user.

        Returns:
            Full name followed by username in parentheses.

        Example:
            >>> profile = UserProfile(
            ...     username="johndoe",
            ...     email="john@example.com",
            ...     full_name="John Doe",
            ...     created_at=datetime.now()
            ... )
            >>> profile.get_display_name()
            'John Doe (@johndoe)'
        """
        return f"{self.full_name} (@{self.username})"

    def has_bio(self) -> bool:
        """Check if user has a biography.

        Returns:
            True if bio is set and not empty, False otherwise.
        """
        return self.bio is not None and len(self.bio.strip()) > 0
