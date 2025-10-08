"""Tests for UserProfile dataclass.

Demonstrates TDD with immutable dataclasses:
- Testing validation in __post_init__
- Testing immutability (frozen=True)
- Comprehensive edge cases
"""

import pytest
from datetime import datetime
from dataclasses import FrozenInstanceError
from src.Python.models.user_profile import UserProfile


class TestUserProfile:
    """Test suite for UserProfile dataclass."""

    @pytest.fixture
    def valid_profile_data(self) -> dict:
        """Fixture providing valid profile data."""
        return {
            "username": "johndoe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "created_at": datetime(2024, 1, 1, 12, 0, 0),
        }

    def test_create_valid_profile_succeeds(self, valid_profile_data: dict) -> None:
        """Test creating a profile with valid data succeeds."""
        # Act
        profile = UserProfile(**valid_profile_data)

        # Assert
        assert profile.username == "johndoe"
        assert profile.email == "john@example.com"
        assert profile.full_name == "John Doe"
        assert profile.bio is None

    def test_profile_is_immutable(self, valid_profile_data: dict) -> None:
        """Test that profile cannot be modified after creation."""
        # Arrange
        profile = UserProfile(**valid_profile_data)

        # Act & Assert
        with pytest.raises(FrozenInstanceError):
            profile.username = "newname"  # type: ignore

        with pytest.raises(FrozenInstanceError):
            profile.email = "new@example.com"  # type: ignore

    @pytest.mark.parametrize(
        "username,expected_error",
        [
            ("", "Username must be at least 3 characters"),
            ("ab", "Username must be at least 3 characters"),
        ],
    )
    def test_invalid_username_raises_error(
        self, valid_profile_data: dict, username: str, expected_error: str
    ) -> None:
        """Test that invalid usernames raise ValueError."""
        # Arrange
        valid_profile_data["username"] = username

        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            UserProfile(**valid_profile_data)

    @pytest.mark.parametrize(
        "email,expected_error",
        [
            ("", "Invalid email address"),
            ("notanemail", "Invalid email address"),
            ("missing-at-sign.com", "Invalid email address"),
        ],
    )
    def test_invalid_email_raises_error(
        self, valid_profile_data: dict, email: str, expected_error: str
    ) -> None:
        """Test that invalid emails raise ValueError."""
        # Arrange
        valid_profile_data["email"] = email

        # Act & Assert
        with pytest.raises(ValueError, match=expected_error):
            UserProfile(**valid_profile_data)

    def test_empty_full_name_raises_error(self, valid_profile_data: dict) -> None:
        """Test that empty full name raises ValueError."""
        # Arrange
        valid_profile_data["full_name"] = ""

        # Act & Assert
        with pytest.raises(ValueError, match="Full name is required"):
            UserProfile(**valid_profile_data)

    def test_get_display_name_returns_correct_format(
        self, valid_profile_data: dict
    ) -> None:
        """Test that display name is formatted correctly."""
        # Arrange
        profile = UserProfile(**valid_profile_data)

        # Act
        display_name = profile.get_display_name()

        # Assert
        assert display_name == "John Doe (@johndoe)"

    @pytest.mark.parametrize(
        "bio,expected",
        [
            (None, False),
            ("", False),
            ("   ", False),
            ("A short bio", True),
            ("  Bio with spaces  ", True),
        ],
    )
    def test_has_bio_returns_correct_value(
        self, valid_profile_data: dict, bio: str | None, expected: bool
    ) -> None:
        """Test that has_bio correctly identifies bio presence."""
        # Arrange
        valid_profile_data["bio"] = bio
        profile = UserProfile(**valid_profile_data)

        # Act
        result = profile.has_bio()

        # Assert
        assert result == expected

    def test_profile_with_bio(self, valid_profile_data: dict) -> None:
        """Test creating profile with optional bio."""
        # Arrange
        valid_profile_data["bio"] = "Software developer and open source enthusiast"

        # Act
        profile = UserProfile(**valid_profile_data)

        # Assert
        assert profile.bio == "Software developer and open source enthusiast"
        assert profile.has_bio() is True

    def test_profiles_with_same_data_are_equal(
        self, valid_profile_data: dict
    ) -> None:
        """Test that dataclass equality works correctly."""
        # Arrange
        profile1 = UserProfile(**valid_profile_data)
        profile2 = UserProfile(**valid_profile_data)

        # Act & Assert
        assert profile1 == profile2

    def test_profile_is_hashable(self, valid_profile_data: dict) -> None:
        """Test that frozen dataclass is hashable and can be used in sets."""
        # Arrange
        profile1 = UserProfile(**valid_profile_data)
        profile2 = UserProfile(**valid_profile_data)

        # Act
        profile_set = {profile1, profile2}

        # Assert - same profiles should be deduplicated in set
        assert len(profile_set) == 1
