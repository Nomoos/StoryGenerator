namespace PrismQ.Shared.Core.Utils;

/// <summary>
/// Configuration for story generation paths.
/// Ported from Python Tools/Utils.py path constants.
/// </summary>
public class PathConfiguration
{
    /// <summary>
    /// Gets or sets the root directory for all story generation.
    /// </summary>
    public string StoryRoot { get; set; } = "./Stories";

    /// <summary>
    /// Gets the path for story ideas.
    /// </summary>
    public string IdeasPath => Path.Combine(StoryRoot, "0_Ideas");

    /// <summary>
    /// Gets the path for generated scripts.
    /// </summary>
    public string ScriptsPath => Path.Combine(StoryRoot, "1_Scripts");

    /// <summary>
    /// Gets the path for revised scripts.
    /// </summary>
    public string RevisedPath => Path.Combine(StoryRoot, "2_Revised");

    /// <summary>
    /// Gets the path for voiceover files.
    /// </summary>
    public string VoiceoverPath => Path.Combine(StoryRoot, "3_VoiceOver");

    /// <summary>
    /// Gets the path for subtitle files.
    /// </summary>
    public string TitlesPath => Path.Combine(StoryRoot, "4_Titles");

    /// <summary>
    /// Gets the path for final video files.
    /// </summary>
    public string VideosPath => Path.Combine(StoryRoot, "5_Videos");

    /// <summary>
    /// Gets the path for resources (images, music, etc.).
    /// </summary>
    public string ResourcesPath => Path.Combine(StoryRoot, "Resources");

    /// <summary>
    /// Gets the filename for revised scripts.
    /// </summary>
    public string RevisedFileName => "Revised.txt";

    /// <summary>
    /// Gets the filename for enhanced scripts with tags.
    /// </summary>
    public string EnhancedFileName => "Revised_with_eleven_labs_tags.txt";

    /// <summary>
    /// Gets the filename for subtitles.
    /// </summary>
    public string SubtitlesFileName => "Subtitles.txt";

    /// <summary>
    /// Gets the filename for word-by-word subtitles.
    /// </summary>
    public string SubtitlesWordByWordFileName => "Subtitles_Word_By_Word.txt";

    /// <summary>
    /// Ensures all required directories exist.
    /// </summary>
    public void EnsureDirectoriesExist()
    {
        var directories = new[]
        {
            IdeasPath,
            ScriptsPath,
            RevisedPath,
            VoiceoverPath,
            TitlesPath,
            VideosPath,
            ResourcesPath
        };

        foreach (var directory in directories)
        {
            FileHelper.EnsureDirectoryExists(directory);
        }
    }

    /// <summary>
    /// Gets the story folder path for a given story title.
    /// </summary>
    /// <param name="basePath">Base path (e.g., ScriptsPath).</param>
    /// <param name="storyTitle">Story title.</param>
    /// <returns>Full path to the story folder.</returns>
    public string GetStoryFolderPath(string basePath, string storyTitle)
    {
        return Path.Combine(basePath, FileHelper.SanitizeFilename(storyTitle));
    }
}
