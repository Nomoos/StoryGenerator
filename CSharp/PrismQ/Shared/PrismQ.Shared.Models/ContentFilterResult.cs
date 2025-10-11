using System.Collections.Generic;

namespace PrismQ.Shared.Models
{
    /// <summary>
    /// Result of content filtering.
    /// </summary>
    public class ContentFilterResult
    {
        public bool IsClean { get; set; }
        public List<FlaggedWord> FlaggedWords { get; set; } = new List<FlaggedWord>();
        public string Message { get; set; } = string.Empty;
    }

    /// <summary>
    /// Information about a flagged word.
    /// </summary>
    public class FlaggedWord
    {
        public string Word { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public FlagSeverity Severity { get; set; }
        public string Context { get; set; } = string.Empty;
    }

    /// <summary>
    /// Severity levels for flagged content.
    /// </summary>
    public enum FlagSeverity
    {
        Low,
        Medium,
        High
    }
}
