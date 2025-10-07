using System.Threading;
using System.Threading.Tasks;

namespace StoryGenerator.Interfaces
{
    /// <summary>
    /// Interface for recommending narrator voice gender based on title and audience.
    /// Provides content-aware voice recommendations with reasoning.
    /// </summary>
    public interface IVoiceRecommender
    {
        /// <summary>
        /// Recommend narrator voice gender for a title.
        /// </summary>
        /// <param name="title">The video title</param>
        /// <param name="targetGender">Target audience gender</param>
        /// <param name="targetAge">Target audience age range</param>
        /// <param name="cancellationToken">Cancellation token</param>
        /// <returns>Voice recommendation with gender and reasoning</returns>
        Task<VoiceRecommendation> RecommendVoiceAsync(
            string title, 
            string targetGender, 
            string targetAge, 
            CancellationToken cancellationToken = default);

        /// <summary>
        /// Get voice recommendation based on content type/genre.
        /// </summary>
        /// <param name="contentType">Type of content (mystery, beauty, tech, etc.)</param>
        /// <param name="targetGender">Target audience gender</param>
        /// <returns>Recommended voice gender</returns>
        VoiceGender GetVoiceByContentType(string contentType, string targetGender);

        /// <summary>
        /// Generate reasoning for a voice recommendation.
        /// </summary>
        /// <param name="title">The video title</param>
        /// <param name="targetGender">Target audience gender</param>
        /// <param name="targetAge">Target audience age range</param>
        /// <param name="recommendedVoice">The recommended voice gender</param>
        /// <returns>Reasoning explanation</returns>
        string GenerateReasoning(
            string title, 
            string targetGender, 
            string targetAge, 
            VoiceGender recommendedVoice);
    }
}
