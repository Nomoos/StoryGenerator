using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using StoryGenerator.Core.Interfaces;

namespace StoryGenerator.Examples.ModelClients
{
    /// <summary>
    /// Example implementation of ISpeechRecognitionClient using Python interop.
    /// This shows how to call Python's faster-whisper from C# using process execution.
    /// </summary>
    /// <remarks>
    /// For production use, consider:
    /// - Python.NET for tighter integration
    /// - gRPC service for better scalability
    /// - Direct ONNX Runtime integration
    /// </remarks>
    public class FasterWhisperClientExample : ISpeechRecognitionClient
    {
        private readonly string _pythonPath;
        private readonly string _scriptPath;
        private readonly string _modelName;

        public FasterWhisperClientExample(
            string pythonPath = "python",
            string scriptPath = "./scripts/faster_whisper_service.py",
            string modelName = "large-v3")
        {
            _pythonPath = pythonPath;
            _scriptPath = scriptPath;
            _modelName = modelName;
        }

        public async Task<TranscriptionResult> TranscribeAsync(
            string audioPath,
            string? language = null,
            int beamSize = 5,
            bool wordTimestamps = true,
            CancellationToken cancellationToken = default)
        {
            // Build command arguments
            var args = new List<string>
            {
                _scriptPath,
                "transcribe",
                audioPath,
                "--model", _modelName,
                "--beam-size", beamSize.ToString()
            };

            if (language != null)
            {
                args.Add("--language");
                args.Add(language);
            }

            if (wordTimestamps)
            {
                args.Add("--word-timestamps");
            }

            // Execute Python script
            var result = await ExecutePythonScriptAsync(args, cancellationToken);

            // Parse JSON response
            var transcription = JsonSerializer.Deserialize<TranscriptionResult>(result)
                ?? throw new InvalidOperationException("Failed to parse transcription result");

            return transcription;
        }

        public async Task<string> TranscribeToSrtAsync(
            string audioPath,
            string outputPath,
            string? language = null,
            int maxWordsPerLine = 10,
            CancellationToken cancellationToken = default)
        {
            var args = new List<string>
            {
                _scriptPath,
                "transcribe-srt",
                audioPath,
                outputPath,
                "--model", _modelName,
                "--max-words", maxWordsPerLine.ToString()
            };

            if (language != null)
            {
                args.Add("--language");
                args.Add(language);
            }

            await ExecutePythonScriptAsync(args, cancellationToken);
            return outputPath;
        }

        public async Task<LanguageDetectionResult> DetectLanguageAsync(
            string audioPath,
            CancellationToken cancellationToken = default)
        {
            var args = new List<string>
            {
                _scriptPath,
                "detect-language",
                audioPath,
                "--model", _modelName
            };

            var result = await ExecutePythonScriptAsync(args, cancellationToken);
            var detection = JsonSerializer.Deserialize<LanguageDetectionResult>(result)
                ?? throw new InvalidOperationException("Failed to parse language detection result");

            return detection;
        }

        public ModelInfo GetModelInfo()
        {
            return new ModelInfo
            {
                Name = "faster-whisper",
                Version = _modelName,
                Size = "large-v3",
                Device = "cuda", // Would detect actual device
                ComputeType = "float16",
                SupportedLanguages = new List<string> { "en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "ja", "ko", "zh" }
            };
        }

        /// <summary>
        /// Execute Python script and capture output.
        /// </summary>
        private async Task<string> ExecutePythonScriptAsync(
            List<string> args,
            CancellationToken cancellationToken)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = _pythonPath,
                Arguments = string.Join(" ", args),
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = startInfo };
            
            var outputBuilder = new System.Text.StringBuilder();
            var errorBuilder = new System.Text.StringBuilder();

            process.OutputDataReceived += (sender, e) =>
            {
                if (e.Data != null)
                    outputBuilder.AppendLine(e.Data);
            };

            process.ErrorDataReceived += (sender, e) =>
            {
                if (e.Data != null)
                    errorBuilder.AppendLine(e.Data);
            };

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            // Wait for process to complete or cancellation
            await process.WaitForExitAsync(cancellationToken);

            if (process.ExitCode != 0)
            {
                throw new InvalidOperationException(
                    $"Python script failed with exit code {process.ExitCode}: {errorBuilder}");
            }

            return outputBuilder.ToString();
        }
    }

    /// <summary>
    /// Example Python script content (save as faster_whisper_service.py):
    /// </summary>
    public static class PythonScriptTemplate
    {
        public const string FasterWhisperService = @"
#!/usr/bin/env python3
""""""
Example Python script for faster-whisper integration.
Usage: python faster_whisper_service.py transcribe audio.mp3 --model large-v3
""""""

import argparse
import json
import sys
from faster_whisper import WhisperModel

def transcribe(args):
    model = WhisperModel(args.model, device='cuda', compute_type='float16')
    
    segments, info = model.transcribe(
        args.audio_path,
        language=args.language,
        beam_size=args.beam_size,
        word_timestamps=args.word_timestamps
    )
    
    result = {
        'text': '',
        'language': info.language,
        'languageConfidence': info.language_probability,
        'segments': [],
        'duration': info.duration
    }
    
    for segment in segments:
        segment_dict = {
            'id': segment.id,
            'start': segment.start,
            'end': segment.end,
            'text': segment.text,
            'confidence': segment.avg_logprob
        }
        
        if args.word_timestamps and segment.words:
            segment_dict['words'] = [
                {
                    'word': word.word,
                    'start': word.start,
                    'end': word.end,
                    'confidence': word.probability
                }
                for word in segment.words
            ]
        
        result['segments'].append(segment_dict)
        result['text'] += segment.text
    
    print(json.dumps(result))

def transcribe_to_srt(args):
    # Implementation for SRT generation
    pass

def detect_language(args):
    model = WhisperModel(args.model, device='cuda', compute_type='float16')
    language, probability = model.detect_language(args.audio_path)
    
    result = {
        'language': language,
        'confidence': probability,
        'alternatives': {}
    }
    
    print(json.dumps(result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    # Transcribe command
    transcribe_parser = subparsers.add_parser('transcribe')
    transcribe_parser.add_argument('audio_path')
    transcribe_parser.add_argument('--model', default='large-v3')
    transcribe_parser.add_argument('--language', default=None)
    transcribe_parser.add_argument('--beam-size', type=int, default=5)
    transcribe_parser.add_argument('--word-timestamps', action='store_true')
    
    # Transcribe to SRT command
    srt_parser = subparsers.add_parser('transcribe-srt')
    srt_parser.add_argument('audio_path')
    srt_parser.add_argument('output_path')
    srt_parser.add_argument('--model', default='large-v3')
    srt_parser.add_argument('--language', default=None)
    srt_parser.add_argument('--max-words', type=int, default=10)
    
    # Detect language command
    detect_parser = subparsers.add_parser('detect-language')
    detect_parser.add_argument('audio_path')
    detect_parser.add_argument('--model', default='large-v3')
    
    args = parser.parse_args()
    
    if args.command == 'transcribe':
        transcribe(args)
    elif args.command == 'transcribe-srt':
        transcribe_to_srt(args)
    elif args.command == 'detect-language':
        detect_language(args)
    else:
        parser.print_help()
        sys.exit(1)
";
    }
}
