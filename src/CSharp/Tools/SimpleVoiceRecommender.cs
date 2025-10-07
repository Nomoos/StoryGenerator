using System;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Interfaces;
using StoryGenerator.Models;

namespace StoryGenerator.Tools
{
    /// <summary>
    /// Simple voice recommender that makes content-aware voice recommendations.
    /// </summary>
    public class SimpleVoiceRecommender : IVoiceRecommender
    {
        /// <summary>
        /// Recommend narrator voice gender for a title.
        /// </summary>
        public Task<VoiceRecommendation> RecommendVoiceAsync(
            string title,
            string targetGender,
            string targetAge,
            CancellationToken cancellationToken = default)
        {
            var voiceGender = GetVoiceByContentType(title, targetGender);
            var reasoning = GenerateReasoning(title, targetGender, targetAge, voiceGender);

            return Task.FromResult(new VoiceRecommendation(voiceGender, reasoning));
        }

        /// <summary>
        /// Get voice recommendation based on content type/genre.
        /// </summary>
        public VoiceGender GetVoiceByContentType(string contentType, string targetGender)
        {
            if (string.IsNullOrWhiteSpace(contentType) || string.IsNullOrWhiteSpace(targetGender))
            {
                return VoiceGender.Female; // Default to female
            }

            var content = contentType.ToLowerInvariant();
            var audience = targetGender.ToLowerInvariant();

            // Tech, gaming, sports typically use male voices
            if (content.Contains("tech") || content.Contains("gaming") || 
                content.Contains("sport") || content.Contains("car") ||
                content.Contains("fitness") || content.Contains("military"))
            {
                return VoiceGender.Male;
            }

            // Beauty, fashion, lifestyle typically use female voices
            if (content.Contains("beauty") || content.Contains("makeup") ||
                content.Contains("fashion") || content.Contains("lifestyle") ||
                content.Contains("wellness") || content.Contains("parenting"))
            {
                return VoiceGender.Female;
            }

            // Mystery, horror can use either but often male for gravitas
            if (content.Contains("mystery") || content.Contains("horror") ||
                content.Contains("crime") || content.Contains("thriller"))
            {
                return VoiceGender.Male;
            }

            // Educational content matches audience gender
            if (content.Contains("education") || content.Contains("tutorial") ||
                content.Contains("how to") || content.Contains("learn"))
            {
                return audience.Contains("women") || audience.Contains("female") 
                    ? VoiceGender.Female 
                    : VoiceGender.Male;
            }

            // For general content, match the target audience gender
            if (audience.Contains("women") || audience.Contains("female"))
            {
                return VoiceGender.Female;
            }
            else if (audience.Contains("men") || audience.Contains("male"))
            {
                return VoiceGender.Male;
            }

            // Default to female for broader appeal
            return VoiceGender.Female;
        }

        /// <summary>
        /// Generate reasoning for a voice recommendation.
        /// </summary>
        public string GenerateReasoning(
            string title,
            string targetGender,
            string targetAge,
            VoiceGender recommendedVoice)
        {
            return $"Recommended {recommendedVoice} voice for '{title}' targeting {targetGender} aged {targetAge} " +
                   $"based on content analysis and audience demographics.";
        }
    }
}
