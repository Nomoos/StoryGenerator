namespace StoryGenerator.Research
{
    /// <summary>
    /// Represents a chat message in the conversation.
    /// </summary>
    public class ChatMessage
    {
        /// <summary>
        /// Role of the message sender (e.g., "user", "assistant", "system").
        /// </summary>
        public string Role { get; set; } = string.Empty;

        /// <summary>
        /// Content of the message.
        /// </summary>
        public string Content { get; set; } = string.Empty;
    }

    /// <summary>
    /// Result of audio transcription using Whisper.
    /// </summary>
    public class TranscriptionResult
    {
        /// <summary>
        /// Full transcribed text.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Detected language code (e.g., "en", "es").
        /// </summary>
        public string Language { get; set; } = string.Empty;

        /// <summary>
        /// Language detection probability (0.0 - 1.0).
        /// </summary>
        public double LanguageProbability { get; set; }

        /// <summary>
        /// Duration of the audio in seconds.
        /// </summary>
        public double Duration { get; set; }

        /// <summary>
        /// Segmented transcription with word-level timestamps.
        /// </summary>
        public List<TranscriptionSegment>? Segments { get; set; }

        /// <summary>
        /// All word-level timestamps (flat list).
        /// </summary>
        public List<WordTimestamp>? Words { get; set; }
    }

    /// <summary>
    /// Represents a segment of transcribed text with timing information.
    /// </summary>
    public class TranscriptionSegment
    {
        /// <summary>
        /// Segment ID.
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Start time in seconds.
        /// </summary>
        public double Start { get; set; }

        /// <summary>
        /// End time in seconds.
        /// </summary>
        public double End { get; set; }

        /// <summary>
        /// Transcribed text for this segment.
        /// </summary>
        public string Text { get; set; } = string.Empty;

        /// <summary>
        /// Confidence score for this segment (0.0 - 1.0).
        /// </summary>
        public double? Confidence { get; set; }

        /// <summary>
        /// Word-level timestamps.
        /// </summary>
        public List<WordTimestamp>? Words { get; set; }
    }

    /// <summary>
    /// Represents a word with its timing information.
    /// </summary>
    public class WordTimestamp
    {
        /// <summary>
        /// Word text.
        /// </summary>
        public string Word { get; set; } = string.Empty;

        /// <summary>
        /// Start time in seconds.
        /// </summary>
        public double Start { get; set; }

        /// <summary>
        /// End time in seconds.
        /// </summary>
        public double End { get; set; }

        /// <summary>
        /// Confidence score (0.0 - 1.0).
        /// </summary>
        public double Confidence { get; set; }
    }

    /// <summary>
    /// Result of audio normalization operation.
    /// </summary>
    public class NormalizationResult
    {
        /// <summary>
        /// Whether normalization was successful.
        /// </summary>
        public bool Success { get; set; }

        /// <summary>
        /// Path to the output file.
        /// </summary>
        public string OutputPath { get; set; } = string.Empty;

        /// <summary>
        /// Target LUFS value.
        /// </summary>
        public double TargetLufs { get; set; }

        /// <summary>
        /// Measured input LUFS.
        /// </summary>
        public double InputLufs { get; set; }

        /// <summary>
        /// Measured output LUFS.
        /// </summary>
        public double OutputLufs { get; set; }

        /// <summary>
        /// Whether two-pass normalization was used.
        /// </summary>
        public bool TwoPass { get; set; }

        /// <summary>
        /// Normalization method used.
        /// </summary>
        public string Method { get; set; } = string.Empty;

        /// <summary>
        /// Detailed loudness measurements.
        /// </summary>
        public LoudnessMeasurements? Measurements { get; set; }

        /// <summary>
        /// Error message if normalization failed.
        /// </summary>
        public string? ErrorMessage { get; set; }
    }

    /// <summary>
    /// Represents loudness measurements from FFmpeg loudnorm.
    /// </summary>
    public class LoudnessMeasurements
    {
        /// <summary>
        /// Input integrated loudness.
        /// </summary>
        public string InputI { get; set; } = string.Empty;

        /// <summary>
        /// Input loudness range.
        /// </summary>
        public string InputLra { get; set; } = string.Empty;

        /// <summary>
        /// Input true peak.
        /// </summary>
        public string InputTp { get; set; } = string.Empty;

        /// <summary>
        /// Input threshold.
        /// </summary>
        public string InputThresh { get; set; } = string.Empty;

        /// <summary>
        /// Target offset.
        /// </summary>
        public string TargetOffset { get; set; } = string.Empty;
    }

    /// <summary>
    /// Result of video processing operation.
    /// </summary>
    public class VideoProcessingResult
    {
        /// <summary>
        /// Whether processing was successful.
        /// </summary>
        public bool Success { get; set; }

        /// <summary>
        /// Path to the output file.
        /// </summary>
        public string OutputPath { get; set; } = string.Empty;

        /// <summary>
        /// Output video width.
        /// </summary>
        public int Width { get; set; }

        /// <summary>
        /// Output video height.
        /// </summary>
        public int Height { get; set; }

        /// <summary>
        /// Duration in seconds.
        /// </summary>
        public double Duration { get; set; }

        /// <summary>
        /// Error message if processing failed.
        /// </summary>
        public string? ErrorMessage { get; set; }
    }

    /// <summary>
    /// Audio file information.
    /// </summary>
    public class AudioInfo
    {
        /// <summary>
        /// Duration in seconds.
        /// </summary>
        public double Duration { get; set; }

        /// <summary>
        /// Sample rate in Hz.
        /// </summary>
        public int SampleRate { get; set; }

        /// <summary>
        /// Number of audio channels.
        /// </summary>
        public int Channels { get; set; }

        /// <summary>
        /// Bitrate in bits per second.
        /// </summary>
        public int Bitrate { get; set; }

        /// <summary>
        /// Bitrate in bits per second (alternate property name).
        /// </summary>
        public int BitRate
        {
            get => Bitrate;
            set => Bitrate = value;
        }

        /// <summary>
        /// Audio codec name.
        /// </summary>
        public string Codec { get; set; } = string.Empty;
    }

    /// <summary>
    /// Result of title scoring.
    /// </summary>
    public class TitleScore
    {
        /// <summary>
        /// Total score (0-100).
        /// </summary>
        public int Total { get; set; }

        /// <summary>
        /// Novelty score (0-25).
        /// </summary>
        public int Novelty { get; set; }

        /// <summary>
        /// Emotional score (0-25).
        /// </summary>
        public int Emotional { get; set; }

        /// <summary>
        /// Clarity score (0-20).
        /// </summary>
        public int Clarity { get; set; }

        /// <summary>
        /// Replay value score (0-15).
        /// </summary>
        public int Replay { get; set; }

        /// <summary>
        /// Share potential score (0-15).
        /// </summary>
        public int Share { get; set; }

        /// <summary>
        /// Rationale for the scores.
        /// </summary>
        public string Rationale { get; set; } = string.Empty;
    }

    /// <summary>
    /// Combined result of transcription and normalization.
    /// </summary>
    public class AudioProcessingResult
    {
        /// <summary>
        /// Whether processing was successful.
        /// </summary>
        public bool Success { get; set; }

        /// <summary>
        /// Path to normalized audio file.
        /// </summary>
        public string NormalizedAudioPath { get; set; } = string.Empty;

        /// <summary>
        /// Transcribed text.
        /// </summary>
        public string TranscriptionText { get; set; } = string.Empty;

        /// <summary>
        /// Path to subtitle file (if generated).
        /// </summary>
        public string SubtitlePath { get; set; } = string.Empty;

        /// <summary>
        /// Detected language.
        /// </summary>
        public string Language { get; set; } = string.Empty;

        /// <summary>
        /// Audio duration in seconds.
        /// </summary>
        public double Duration { get; set; }

        /// <summary>
        /// When processing was completed.
        /// </summary>
        public DateTime ProcessedAt { get; set; }

        /// <summary>
        /// Transcription result (detailed).
        /// </summary>
        public TranscriptionResult? Transcription { get; set; }

        /// <summary>
        /// Normalized audio result (detailed).
        /// </summary>
        public NormalizationResult? NormalizedAudio { get; set; }
    }
}
