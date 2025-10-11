namespace PrismQ.Shared.Interfaces;

/// <summary>
/// Base interface for all generators in the pipeline.
/// </summary>
public interface IGenerator
{
    /// <summary>
    /// Gets the name of the generator.
    /// </summary>
    string Name { get; }

    /// <summary>
    /// Gets the version of the generator.
    /// </summary>
    string Version { get; }
}
