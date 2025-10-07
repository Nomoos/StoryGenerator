# StoryGenerator CLI

Command-line interface for the StoryGenerator content creation pipeline.

## Installation

```bash
cd CSharp/StoryGenerator.CLI
dotnet build
```

## Configuration

Set the following environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export ELEVENLABS_API_KEY="your-elevenlabs-key"
export ELEVENLABS_VOICE_ID="your-voice-id"  # Optional, defaults to BZgkqPqms7Kj9ulSkVzn
export STORY_ROOT="./Stories"  # Optional, defaults to ./Stories
```

## Commands

### Generate Story Ideas

Generate story ideas with viral potential scoring:

```bash
./StoryGenerator.CLI generate-ideas \
  --topic "A person who discovers something unexpected" \
  --count 5 \
  --tone "emotional" \
  --theme "friendship" \
  --output "./0_Ideas"
```

### Generate Script

Generate a ~360 word script from a story idea:

```bash
./StoryGenerator.CLI generate-script \
  --idea-file "./0_Ideas/my-story.json" \
  --output "./1_Scripts"
```

### Revise Script

Revise a script for AI voice clarity:

```bash
./StoryGenerator.CLI revise-script \
  --script-dir "./1_Scripts/My-Story" \
  --output "./2_Revised" \
  --title "My Story"
```

### Enhance Script

Add ElevenLabs voice tags to a revised script:

```bash
./StoryGenerator.CLI enhance-script \
  --revised-dir "./2_Revised/My-Story" \
  --title "My Story"
```

### Generate Voice

Generate voiceover audio from a script:

```bash
./StoryGenerator.CLI generate-voice \
  --script "./2_Revised/My-Story/Revised_with_eleven_labs_tags.txt" \
  --output "./voiceover.mp3" \
  --stability 0.7
```

### Generate Subtitles

Generate word-level SRT subtitles:

```bash
./StoryGenerator.CLI generate-subtitles \
  --audio "./voiceover.mp3" \
  --script "./2_Revised/My-Story/Revised.txt" \
  --output "./subtitles.srt"
```

### Full Pipeline

Run the complete pipeline from idea to audio with subtitles:

```bash
./StoryGenerator.CLI full-pipeline \
  --topic "A person who discovers something unexpected" \
  --output-root "./Stories"
```

This will:
1. Generate a story idea
2. Create a script
3. Revise the script
4. Enhance with voice tags
5. Generate voiceover audio
6. Create word-level subtitles

## Example Output

```
🚀 Starting full pipeline...

1️⃣  Generating story idea...
   ✅ The Hidden Letter

2️⃣  Generating script...
   ✅ ./Stories/1_Scripts/The-Hidden-Letter/Script.txt

3️⃣  Revising script...
   ✅ ./Stories/2_Revised/The-Hidden-Letter/Revised.txt

4️⃣  Enhancing script with voice tags...
   ✅ ./Stories/2_Revised/The-Hidden-Letter/Revised_with_eleven_labs_tags.txt

5️⃣  Generating voiceover...
   ✅ ./Stories/2_Revised/The-Hidden-Letter/voiceover.mp3

6️⃣  Generating subtitles...
   ✅ ./Stories/2_Revised/The-Hidden-Letter/subtitles.srt
      Words: 362, Accuracy: 95.3%

🎉 Pipeline complete!
📂 Output directory: ./Stories/2_Revised/The-Hidden-Letter
```

## Architecture

The CLI uses:
- **System.CommandLine** for command-line parsing
- **Microsoft.Extensions.DependencyInjection** for dependency injection
- **Microsoft.Extensions.Logging** for structured logging

All generators are configured with:
- Retry logic with exponential backoff
- Circuit breakers for API resilience
- Performance monitoring
- Structured error handling

## Development

Build the project:
```bash
dotnet build
```

Run from source:
```bash
dotnet run -- generate-ideas --topic "test" --count 1
```

Publish as single executable:
```bash
dotnet publish -c Release -r linux-x64 --self-contained
```

## Troubleshooting

**Error: OPENAI_API_KEY environment variable not set**
- Set the environment variable before running the CLI

**Error: No response from OpenAI**
- Check your API key and quota
- Verify network connectivity

**Error: Failed to deserialize transcription response**
- Ensure audio file is in supported format (MP3, WAV, etc.)
- Check audio file size (max 25MB for Whisper API)

## License

See main repository LICENSE file.
