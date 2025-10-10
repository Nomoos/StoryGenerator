using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Models;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for complete video production from keyframes, subtitles, script/text, and other sources.
    /// Orchestrates the entire video production pipeline.
    /// </summary>
    public interface IVideoProducer
    {
        /// <summary>
        /// Produce a complete video from keyframes, subtitles, script/text, and audio sources.
        /// </summary>
        /// <param name="config">Video production configuration</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Result containing the produced video path and metadata</returns>
        Task<VideoProductionResult> ProduceVideoAsync(
            VideoProductionConfig config,
            CancellationToken cancellationToken = default);
    }
}
