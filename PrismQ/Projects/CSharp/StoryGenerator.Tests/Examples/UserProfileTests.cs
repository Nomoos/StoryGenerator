using Xunit;

namespace StoryGenerator.Tests.Examples;

/// <summary>
/// Tests for UserProfile record.
/// Demonstrates testing immutable records with validation.
/// </summary>
public class UserProfileTests
{
    private static DateTime TestDate => new(2024, 1, 1, 12, 0, 0);

    [Fact]
    public void Constructor_ValidData_CreatesProfile()
    {
        // Arrange & Act
        var profile = UserProfile.Create(
            username: "johndoe",
            email: "john@example.com",
            fullName: "John Doe",
            createdAt: TestDate);

        // Assert
        Assert.Equal("johndoe", profile.Username);
        Assert.Equal("john@example.com", profile.Email);
        Assert.Equal("John Doe", profile.FullName);
        Assert.Null(profile.Bio);
    }

    [Theory]
    [InlineData(null)]
    public void Constructor_NullUsername_ThrowsArgumentNullException(string? username)
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() =>
            UserProfile.Create(username!, "test@example.com", "Test User", TestDate));
    }

    [Theory]
    [InlineData("")]
    [InlineData("ab")]
    public void Constructor_InvalidUsername_ThrowsArgumentException(string username)
    {
        // Act & Assert
        var exception = Assert.Throws<ArgumentException>(() =>
            UserProfile.Create(username, "test@example.com", "Test User", TestDate));
        Assert.Contains("Username must be at least 3 characters", exception.Message);
    }

    [Theory]
    [InlineData("")]
    [InlineData("notanemail")]
    [InlineData("missing-at-sign.com")]
    public void Constructor_InvalidEmail_ThrowsArgumentException(string email)
    {
        // Act & Assert
        var exception = Assert.Throws<ArgumentException>(() =>
            UserProfile.Create("johndoe", email, "Test User", TestDate));
        Assert.Contains("Invalid email address", exception.Message);
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    public void Constructor_InvalidFullName_ThrowsArgumentException(string? fullName)
    {
        // Act & Assert
        var exception = Assert.Throws<ArgumentException>(() =>
            UserProfile.Create("johndoe", "test@example.com", fullName!, TestDate));
        Assert.Contains("Full name is required", exception.Message);
    }

    [Fact]
    public void Constructor_NullFullName_ThrowsArgumentNullException()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() =>
            UserProfile.Create("johndoe", "test@example.com", null!, TestDate));
    }

    [Fact]
    public void GetDisplayName_ReturnsCorrectFormat()
    {
        // Arrange
        var profile = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);

        // Act
        var displayName = profile.GetDisplayName();

        // Assert
        Assert.Equal("John Doe (@johndoe)", displayName);
    }

    [Theory]
    [InlineData(null, false)]
    [InlineData("", false)]
    [InlineData("   ", false)]
    [InlineData("A short bio", true)]
    [InlineData("  Bio with spaces  ", true)]
    public void HasBio_ReturnsCorrectValue(string? bio, bool expected)
    {
        // Arrange
        var profile = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate, bio);

        // Act
        var result = profile.HasBio();

        // Assert
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Record_WithSameData_AreEqual()
    {
        // Arrange
        var profile1 = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);
        var profile2 = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);

        // Act & Assert
        Assert.Equal(profile1, profile2);
        Assert.True(profile1 == profile2);
    }

    [Fact]
    public void Record_WithDifferentData_AreNotEqual()
    {
        // Arrange
        var profile1 = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);
        var profile2 = UserProfile.Create("janedoe", "jane@example.com", "Jane Doe", TestDate);

        // Act & Assert
        Assert.NotEqual(profile1, profile2);
        Assert.False(profile1 == profile2);
    }

    [Fact]
    public void Record_WithExpression_CreatesNewInstance()
    {
        // Arrange
        var original = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);

        // Act - Use 'with' expression to create modified copy
        var modified = original with { Bio = "Software developer" };

        // Assert
        Assert.Equal("johndoe", modified.Username);
        Assert.Equal("Software developer", modified.Bio);
        Assert.Null(original.Bio); // Original unchanged
        Assert.NotSame(original, modified); // Different instances
    }

    [Fact]
    public void Record_IsHashable_CanBeUsedInHashSet()
    {
        // Arrange
        var profile1 = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);
        var profile2 = UserProfile.Create("johndoe", "john@example.com", "John Doe", TestDate);

        // Act
        var profileSet = new HashSet<UserProfile> { profile1, profile2 };

        // Assert - Same records should be deduplicated
        Assert.Single(profileSet);
    }
}
