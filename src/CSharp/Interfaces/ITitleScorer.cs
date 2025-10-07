using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for scoring video titles for viral potential.
    /// Evaluates titles on multiple criteria and provides recommendations.
    /// </summary>
    public interface ITitleScorer
    {
        /// <summary>
        /// Score a single title for viral potential.
        /// </summary>
        /// <param name="title">The video title to score</param>
        /// <param name="targetGender">Target audience gender (men/women)</param>
        /// <param name="targetAge">Target audience age range (e.g., "18-23")</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Title scoring result with score, rationale, and voice recommendation</returns>
        Task<TitleScoringResult> ScoreTitleAsync(
            string title, 
            string targetGender, 
            string targetAge, 
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Score multiple titles for a specific audience segment.
        /// </summary>
        /// <param name="titles">Collection of titles to score</param>
        /// <param name="targetGender">Target audience gender</param>
        /// <param name="targetAge">Target audience age range</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of scoring results</returns>
        Task<IEnumerable<TitleScoringResult>> ScoreTitlesAsync(
            IEnumerable<string> titles, 
            string targetGender, 
            string targetAge, 
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Score all titles found in a specific segment directory.
        /// </summary>
        /// <param name="segment">Audience segment (gender and age)</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Collection of scoring results</returns>
        Task<IEnumerable<TitleScoringResult>> ScoreSegmentAsync(
            AudienceSegment segment, 
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Select the top N titles from a collection of scored titles.
        /// </summary>
        /// <param name="scoredTitles">Collection of scored titles</param>
        /// <param name="count">Number of top titles to select (default: 5)</param>
        /// <returns>Top N titles ordered by score (descending)</returns>
        IEnumerable<TitleScoringResult> SelectTopTitles(
            IEnumerable<TitleScoringResult> scoredTitles, 
            int count = 5);
    }
}
