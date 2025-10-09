namespace StoryGenerator.Core.Interfaces;

/// <summary>
/// Represents an object that can be cloned (deep copy).
/// </summary>
/// <typeparam name="T">Type of the object to clone.</typeparam>
public interface IPrototype<T>
{
    /// <summary>
    /// Creates a deep copy of the object.
    /// </summary>
    /// <returns>A new instance with copied values.</returns>
    T Clone();
}
