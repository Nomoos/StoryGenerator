using System;
using System.Diagnostics;
using System.IO;

namespace StoryGenerator.Research.Tests
{
    /// <summary>
    /// Helper utilities for testing.
    /// </summary>
    public static class TestHelpers
    {
        /// <summary>
        /// Check if whisper_subprocess.py script is available.
        /// </summary>
        public static bool IsWhisperAvailable()
        {
            var possiblePaths = new[]
            {
                "research/python/whisper_subprocess.py",
                Path.Combine("research", "python", "whisper_subprocess.py"),
                "../research/python/whisper_subprocess.py",
                Path.Combine("..", "research", "python", "whisper_subprocess.py"),
                "../../research/python/whisper_subprocess.py",
                Path.Combine("..", "..", "research", "python", "whisper_subprocess.py"),
                "../../../research/python/whisper_subprocess.py",
                Path.Combine("..", "..", "..", "research", "python", "whisper_subprocess.py"),
                "../../../../research/python/whisper_subprocess.py",
                Path.Combine("..", "..", "..", "..", "research", "python", "whisper_subprocess.py"),
                "../../../../../research/python/whisper_subprocess.py",
                Path.Combine("..", "..", "..", "..", "..", "research", "python", "whisper_subprocess.py")
            };

            foreach (var path in possiblePaths)
            {
                try
                {
                    if (File.Exists(path))
                    {
                        return true;
                    }
                }
                catch
                {
                    continue;
                }
            }

            return false;
        }

        /// <summary>
        /// Check if Ollama CLI is available.
        /// </summary>
        public static bool IsOllamaAvailable()
        {
            try
            {
                var startInfo = new ProcessStartInfo
                {
                    FileName = "ollama",
                    Arguments = "--version",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(startInfo);
                if (process != null)
                {
                    process.WaitForExit(5000);
                    return process.ExitCode == 0;
                }
            }
            catch
            {
                // Ollama not found
            }

            return false;
        }

        /// <summary>
        /// Check if FFmpeg is available.
        /// </summary>
        public static bool IsFFmpegAvailable()
        {
            try
            {
                var startInfo = new ProcessStartInfo
                {
                    FileName = "ffmpeg",
                    Arguments = "-version",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(startInfo);
                if (process != null)
                {
                    process.WaitForExit(5000);
                    return process.ExitCode == 0;
                }
            }
            catch
            {
                // FFmpeg not found
            }

            return false;
        }

        /// <summary>
        /// Create a dummy audio file for testing.
        /// </summary>
        public static string CreateDummyAudioFile(string filename = "test_audio.wav")
        {
            var path = Path.Combine(Path.GetTempPath(), filename);
            
            // Create a minimal WAV file header (44 bytes)
            // This is a valid but silent 1-second 16-bit mono 44.1kHz WAV file
            byte[] wavHeader = new byte[]
            {
                // RIFF header
                0x52, 0x49, 0x46, 0x46, // "RIFF"
                0x24, 0xAC, 0x00, 0x00, // File size - 8
                0x57, 0x41, 0x56, 0x45, // "WAVE"
                
                // fmt chunk
                0x66, 0x6D, 0x74, 0x20, // "fmt "
                0x10, 0x00, 0x00, 0x00, // Chunk size (16)
                0x01, 0x00,             // Audio format (1 = PCM)
                0x01, 0x00,             // Number of channels (1 = mono)
                0x44, 0xAC, 0x00, 0x00, // Sample rate (44100)
                0x88, 0x58, 0x01, 0x00, // Byte rate
                0x02, 0x00,             // Block align
                0x10, 0x00,             // Bits per sample (16)
                
                // data chunk
                0x64, 0x61, 0x74, 0x61, // "data"
                0x00, 0xAC, 0x00, 0x00  // Data size
            };

            // Write header and silent audio data (1 second = 44100 samples * 2 bytes)
            using (var fs = new FileStream(path, FileMode.Create))
            {
                fs.Write(wavHeader, 0, wavHeader.Length);
                // Write silent audio (zeros)
                byte[] silence = new byte[44100 * 2];
                fs.Write(silence, 0, silence.Length);
            }

            return path;
        }

        /// <summary>
        /// Create a dummy video file for testing.
        /// </summary>
        public static string CreateDummyVideoFile(string filename = "test_video.mp4")
        {
            // For video files, we can't easily create a valid one without FFmpeg
            // So we'll just create an empty file or skip tests that need it
            var path = Path.Combine(Path.GetTempPath(), filename);
            File.WriteAllText(path, string.Empty);
            return path;
        }

        /// <summary>
        /// Clean up temporary test file.
        /// </summary>
        public static void CleanupFile(string path)
        {
            try
            {
                if (File.Exists(path))
                {
                    File.Delete(path);
                }
            }
            catch
            {
                // Ignore cleanup errors
            }
        }
    }
}
