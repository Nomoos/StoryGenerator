namespace StoryGenerator.Tests.Examples;

/// <summary>
/// Immutable user profile record.
/// Demonstrates C# best practices: using records for DTOs/value objects.
/// </summary>
/// <param name="Username">Unique username for the user.</param>
/// <param name="Email">User's email address.</param>
/// <param name="FullName">User's full name.</param>
/// <param name="CreatedAt">Timestamp of profile creation.</param>
/// <param name="Bio">Optional biography text.</param>
public record UserProfile
{
    /// <summary>
    /// Gets the username.
    /// </summary>
    public required string Username { get; init; }

    /// <summary>
    /// Gets the email address.
    /// </summary>
    public required string Email { get; init; }

    /// <summary>
    /// Gets the full name.
    /// </summary>
    public required string FullName { get; init; }

    /// <summary>
    /// Gets the creation timestamp.
    /// </summary>
    public required DateTime CreatedAt { get; init; }

    /// <summary>
    /// Gets the optional biography.
    /// </summary>
    public string? Bio { get; init; }

    /// <summary>
    /// Initializes a new instance of the <see cref="UserProfile"/> record.
    /// </summary>
    public UserProfile()
    {
    }

    /// <summary>
    /// Factory method to create a validated UserProfile.
    /// </summary>
    /// <param name="username">Unique username for the user.</param>
    /// <param name="email">User's email address.</param>
    /// <param name="fullName">User's full name.</param>
    /// <param name="createdAt">Timestamp of profile creation.</param>
    /// <param name="bio">Optional biography text.</param>
    /// <returns>A validated UserProfile instance.</returns>
    /// <exception cref="ArgumentNullException">Thrown if any required parameter is null.</exception>
    /// <exception cref="ArgumentException">Thrown if validation fails.</exception>
    public static UserProfile Create(
        string username,
        string email,
        string fullName,
        DateTime createdAt,
        string? bio = null)
    {
        ArgumentNullException.ThrowIfNull(username);
        ArgumentNullException.ThrowIfNull(email);
        ArgumentNullException.ThrowIfNull(fullName);

        if (username.Length < 3)
        {
            throw new ArgumentException("Username must be at least 3 characters", nameof(username));
        }

        if (!email.Contains('@'))
        {
            throw new ArgumentException("Invalid email address", nameof(email));
        }

        if (string.IsNullOrWhiteSpace(fullName))
        {
            throw new ArgumentException("Full name is required", nameof(fullName));
        }

        return new UserProfile
        {
            Username = username,
            Email = email,
            FullName = fullName,
            CreatedAt = createdAt,
            Bio = bio
        };
    }

    /// <summary>
    /// Gets the display name for the user.
    /// </summary>
    /// <returns>Full name followed by username in parentheses.</returns>
    public string GetDisplayName() => $"{FullName} (@{Username})";

    /// <summary>
    /// Checks if the user has a biography.
    /// </summary>
    /// <returns>True if bio is set and not empty, false otherwise.</returns>
    public bool HasBio() => !string.IsNullOrWhiteSpace(Bio);
}
