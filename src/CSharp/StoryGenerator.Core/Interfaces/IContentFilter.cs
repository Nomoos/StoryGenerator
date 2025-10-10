namespace StoryGenerator.Core.Services
{
    /// <summary>
    /// Interface for content filtering service.
    /// </summary>
    public interface IContentFilter
    {
        /// <summary>
        /// Check if content contains demonetized words or patterns.
        /// </summary>
        ContentFilterResult CheckContent(string content);

        /// <summary>
        /// Get suggested replacements for flagged content.
        /// </summary>
        string SuggestReplacements(string content, ContentFilterResult filterResult);
    }
}
