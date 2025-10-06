using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for reading and validating title schema data.
    /// Works with title items conforming to the schema defined in /config/schemas/title.json
    /// </summary>
    public interface ITitleSchemaReader
    {
        /// <summary>
        /// Reads and validates title schema items from a JSON file.
        /// </summary>
        /// <param name="filePath">Path to the JSON file containing title schema data</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of validated title schema items</returns>
        Task<IEnumerable<TitleSchema>> ReadTitleSchemasAsync(
            string filePath,
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Validates a title schema item against the schema rules.
        /// </summary>
        /// <param name="titleSchema">Title schema to validate</param>
        /// <returns>True if valid, false otherwise</returns>
        bool ValidateTitleSchema(TitleSchema titleSchema);

        /// <summary>
        /// Validates that a segment value is allowed (women|men).
        /// </summary>
        /// <param name="segment">Segment value to validate</param>
        /// <returns>True if segment is valid</returns>
        bool IsValidSegment(string segment);

        /// <summary>
        /// Validates that an age bucket value is allowed (10-13|14-17|18-23).
        /// </summary>
        /// <param name="ageBucket">Age bucket to validate</param>
        /// <returns>True if age bucket is valid</returns>
        bool IsValidAgeBucket(string ageBucket);

        /// <summary>
        /// Validates that a string is a valid UUID.
        /// </summary>
        /// <param name="id">ID to validate</param>
        /// <returns>True if ID is a valid UUID</returns>
        bool IsValidUuid(string id);
    }
}
