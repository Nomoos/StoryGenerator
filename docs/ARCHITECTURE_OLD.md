# StoryGenerator - Project Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        StoryGenerator                           │
│              AI-Powered Story Generation Pipeline               │
└─────────────────────────────────────────────────────────────────┘
```

## Generation Pipeline

```
     ┌──────────────┐
     │   User Input │
     │   (Topic,    │
     │  Tone, Theme)│
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐        ┌────────────┐
     │ StoryIdeas   │───────>│  OpenAI    │
     │  Generator   │<───────│  GPT-4o    │
     └──────┬───────┘        └────────────┘
            │
            │ Generates 1-5 ideas with viral scores
            ▼
     ┌──────────────┐
     │  Story Idea  │
     │    (JSON)    │
     │ saved to:    │
     │ Stories/     │
     │ 0_Ideas/     │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐        ┌────────────┐
     │    Script    │───────>│  OpenAI    │
     │  Generator   │<───────│  GPT-4o    │
     └──────┬───────┘        └────────────┘
            │
            │ Creates ~360 word script
            ▼
     ┌──────────────┐
     │ Initial      │
     │ Script.txt   │
     │ saved to:    │
     │ Stories/     │
     │ 1_Scripts/   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐        ┌────────────┐
     │   Revised    │───────>│  OpenAI    │
     │    Script    │<───────│  GPT-4o    │
     │  Generator   │        └────────────┘
     └──────┬───────┘
            │
            │ Improves clarity and flow
            ▼
     ┌──────────────┐
     │  Revised.txt │
     │ saved to:    │
     │ Stories/     │
     │ 2_Revised/   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐        ┌────────────┐
     │  Enhance     │───────>│  OpenAI    │
     │   Script     │<───────│  GPT-4o    │
     │  Generator   │        └────────────┘
     └──────┬───────┘
            │
            │ Adds ElevenLabs voice tags
            │ [emotion][reaction][pacing]
            ▼
     ┌──────────────┐
     │ Enhanced.txt │
     │ with tags    │
     │ saved to:    │
     │ Stories/     │
     │ 2_Revised/   │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐        ┌────────────┐
     │    Voice     │───────>│ ElevenLabs │
     │    Maker     │<───────│   API v3   │
     └──────┬───────┘        └────────────┘
            │
            │ Generates voiceover
            │ Normalizes audio (LUFS)
            ▼
     ┌──────────────┐
     │ voiceover    │
     │ normalized   │
     │    .mp3      │
     │ saved to:    │
     │ Stories/     │
     │ 3_VoiceOver/ │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │   Final      │
     │   Output     │
     └──────────────┘
```

## File Structure

```
StoryGenerator/
│
├── 📁 Generators/               # Core generation modules
│   ├── GStoryIdeas.py          # Story idea generation
│   ├── GScript.py              # Initial script writing
│   ├── GRevise.py              # Script revision & polish
│   ├── GEnhanceScript.py       # Add voice performance tags
│   ├── GVoice.py               # Voice generation & audio
│   └── GTitles.py              # Title generation
│
├── 📁 Models/                   # Data models
│   └── StoryIdea.py            # Story idea structure & validation
│
├── 📁 Tools/                    # Utilities
│   └── Utils.py                # Helper functions & constants
│
├── 📁 Generation/              # Manual execution scripts
│   └── Manual/
│       ├── MIdea.py            # Batch idea generation
│       ├── MScript.py          # Batch script generation
│       ├── MRevise.py          # Batch revision
│       ├── MEnhanceScript.py   # Batch enhancement
│       ├── MVoice.py           # Batch voice generation
│       ├── MTitles.py          # Title operations
│       └── MConvertMP3ToMP4.py # Media conversion
│
├── 📁 Stories/                 # Generated content (gitignored)
│   ├── 0_Ideas/                # Story ideas (JSON)
│   ├── 1_Scripts/              # Initial scripts
│   ├── 2_Revised/              # Revised & enhanced scripts
│   └── 3_VoiceOver/            # Audio files
│
├── 📄 Documentation
│   ├── README.md               # Main documentation
│   ├── QUICKSTART.md           # 15-minute setup guide
│   ├── RESEARCH_AND_IMPROVEMENTS.md  # Analysis & roadmap
│   ├── SECURITY_CHECKLIST.md   # Security procedures
│   ├── SUMMARY.md              # Implementation summary
│   └── ARCHITECTURE.md         # This file
│
├── 📄 Configuration
│   ├── .env.example            # Environment template
│   ├── .gitignore              # Git exclusions
│   ├── requirements.txt        # Python dependencies
│   ├── requirements-dev.txt    # Dev dependencies
│   └── pyproject.toml          # Python project config
│
└── 📝 Other
    └── .idea/                  # IDE settings (gitignored)
```

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         External Services                        │
├────────────────┬──────────────────┬────────────────────────────┤
│   OpenAI API   │  ElevenLabs API  │   File System             │
│   (GPT-4o)     │   (Voice Gen)    │   (Local Storage)         │
└────────┬───────┴────────┬─────────┴────────┬──────────────────┘
         │                 │                  │
         │                 │                  │
┌────────▼─────────────────▼──────────────────▼──────────────────┐
│                     StoryGenerator Core                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Generators  │  │    Models    │  │    Tools     │         │
│  │              │  │              │  │              │         │
│  │ - Ideas      │  │ - StoryIdea  │  │ - Utils      │         │
│  │ - Script     │  │              │  │ - Sanitize   │         │
│  │ - Revise     │  │              │  │ - Convert    │         │
│  │ - Enhance    │  │              │  │              │         │
│  │ - Voice      │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
         │                 │                  │
         │                 │                  │
┌────────▼─────────────────▼──────────────────▼──────────────────┐
│                      User Interfaces                            │
├─────────────────────────────────────────────────────────────────┤
│  Python Scripts  │  Future: CLI  │  Future: Web UI             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Topic + Tone + Theme
        │
        ▼
    [StoryIdea JSON]
    {
      "story_title": "...",
      "narrator_gender": "...",
      "tone": "...",
      "theme": "...",
      "potencial": {
        "overall": 78,
        "platforms": {...},
        "regions": {...}
      }
    }
        │
        ▼
    [Script.txt]
    Raw narration text
    ~360 words
        │
        ▼
    [Revised.txt]
    Polished narration
    Better flow and clarity
        │
        ▼
    [Enhanced.txt]
    [hesitates][sad] Text...
    [pause][playfully] More text...
        │
        ▼
    [voiceover.mp3]
    High-quality audio
    Normalized to -14 LUFS
```

## Class Relationships

```
┌─────────────────────┐
│     StoryIdea       │
│  (Data Model)       │
├─────────────────────┤
│ + story_title       │
│ + narrator_gender   │
│ + tone              │
│ + theme             │
│ + potencial         │
├─────────────────────┤
│ + to_file()         │
│ + from_file()       │
│ + calculate_score() │
└──────────┬──────────┘
           │
           │ used by
           │
      ┌────▼──────────────────────────┐
      │                                │
┌─────▼──────────┐  ┌─────▼──────────┐
│StoryIdeas      │  │ Script         │
│Generator       │  │ Generator      │
├────────────────┤  ├────────────────┤
│- model         │  │- model         │
│- openai.api_key│  │- openai.api_key│
├────────────────┤  ├────────────────┤
│+ generate()    │  │+ generate()    │
│+ _build_prompt │  │+ _build_prompt │
└────────────────┘  └─────┬──────────┘
                          │
                          │ produces
                          │
                    ┌─────▼──────────┐
                    │ Revised        │
                    │ Generator      │
                    ├────────────────┤
                    │- model         │
                    ├────────────────┤
                    │+ Revise()      │
                    └─────┬──────────┘
                          │
                          │ feeds into
                          │
                    ┌─────▼──────────┐
                    │ Enhance        │
                    │ Generator      │
                    ├────────────────┤
                    │- model         │
                    ├────────────────┤
                    │+ Enhance()     │
                    └─────┬──────────┘
                          │
                          │ used by
                          │
                    ┌─────▼──────────┐
                    │ VoiceMaker     │
                    ├────────────────┤
                    │- client        │
                    │- elevenlabs    │
                    ├────────────────┤
                    │+ generate()    │
                    │+ normalize()   │
                    └────────────────┘
```

## API Dependencies

```
┌───────────────────────────────────────┐
│         StoryGenerator APIs           │
└───────────────────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
┌───────▼────────┐  ┌────▼───────────┐
│   OpenAI API   │  │ ElevenLabs API │
├────────────────┤  ├────────────────┤
│ Model:         │  │ Model: v3      │
│ gpt-4o-mini    │  │ Voice:         │
│                │  │ BZgkqPq...     │
│ Usage:         │  │                │
│ - Ideas        │  │ Usage:         │
│ - Scripts      │  │ - Voiceover    │
│ - Revision     │  │                │
│ - Enhancement  │  │                │
│                │  │                │
│ Cost:          │  │ Cost:          │
│ $0.001-0.005   │  │ $0.05-0.15     │
│ per story      │  │ per story      │
└────────────────┘  └────────────────┘
```

## Configuration Flow

```
┌─────────────────┐
│   .env file     │
│                 │
│ OPENAI_API_KEY  │
│ ELEVENLABS_KEY  │
│ DEFAULT_MODEL   │
│ TEMPERATURE     │
│ ...             │
└────────┬────────┘
         │
         │ loaded by
         │
┌────────▼────────┐
│  python-dotenv  │
│  load_dotenv()  │
└────────┬────────┘
         │
         │ sets
         │
┌────────▼────────┐
│  Environment    │
│   Variables     │
│                 │
│ os.getenv(...)  │
└────────┬────────┘
         │
         │ used by
         │
┌────────▼────────┐
│   Generators    │
│                 │
│ openai.api_key  │
│ elevenlabs_key  │
└─────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│          Secrets Management             │
└─────────────────────────────────────────┘
         
INSECURE (Current):              SECURE (Recommended):
                                 
┌─────────────┐                 ┌─────────────┐
│  API Keys   │                 │  API Keys   │
│  in Code    │                 │  in .env    │
│     ❌      │                 │     ✅      │
└─────────────┘                 └─────────────┘
      │                                │
      │ Exposed in Git                 │ Not in Git
      │                                │
      ▼                                ▼
┌─────────────┐                 ┌─────────────┐
│ Public Repo │                 │   .env      │
│  Anyone can │                 │  (local)    │
│  see keys   │                 │  .gitignore │
│     ⚠️      │                 │     🔒      │
└─────────────┘                 └─────────────┘
```

## Future Architecture (Recommended)

```
┌─────────────────────────────────────────────────────────────┐
│                    Improved Architecture                     │
└─────────────────────────────────────────────────────────────┘

┌────────────────┐
│  CLI / Web UI  │  ← User Interface
└───────┬────────┘
        │
┌───────▼────────┐
│   API Layer    │  ← RESTful API (Future)
└───────┬────────┘
        │
┌───────▼────────┐
│  Service Layer │  ← Business Logic
│                │
│ - IdeasService │
│ - ScriptService│
│ - VoiceService │
└───────┬────────┘
        │
┌───────▼────────┐
│ Provider Layer │  ← External Services
│                │
│ - OpenAIProvider
│ - ElevenProvider
│ - StorageProvider
└───────┬────────┘
        │
┌───────▼────────┐
│  Config Layer  │  ← Settings & Secrets
│                │
│ - Settings     │
│ - Secrets      │
│ - Logging      │
└────────────────┘
```

## Performance Considerations

```
Current (Synchronous):
Story 1 → [2s] → Story 2 → [2s] → Story 3
Total: 6 seconds for 3 stories

Future (Asynchronous):
Story 1 ─┐
Story 2 ─┼→ [2s parallel] → Complete
Story 3 ─┘
Total: 2 seconds for 3 stories
```

## Monitoring & Logging

```
┌─────────────────────────────────────────┐
│           Future Monitoring             │
└─────────────────────────────────────────┘

Generation Request
        │
        ▼
┌───────────────┐
│ Logger        │ → logs/storygen.log
├───────────────┤
│ - Timestamp   │
│ - Operation   │
│ - Duration    │
│ - Cost        │
│ - Status      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Metrics       │ → Dashboard
├───────────────┤
│ - API Calls   │
│ - Total Cost  │
│ - Avg Time    │
│ - Error Rate  │
└───────────────┘
```

---

## Key Architectural Decisions

### 1. Pipeline Design
- **Linear flow**: Idea → Script → Revise → Enhance → Voice
- **File-based**: Each stage saves to disk
- **Pro**: Simple, debuggable, resumable
- **Con**: Not optimized for batch processing

### 2. External Dependencies
- **OpenAI**: For all text generation
- **ElevenLabs**: For voice synthesis
- **Pro**: Best-in-class quality
- **Con**: Dependent on external services and pricing

### 3. Storage
- **Local file system**: JSON + TXT files
- **Pro**: Simple, version-controllable
- **Con**: Not scalable for large volumes

### 4. Configuration
- **Current**: Hardcoded values
- **Future**: Environment variables + config files
- **Recommended**: Both for flexibility

## See Also

- [README.md](README.md) - Setup and usage
- [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md) - Detailed analysis
- [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) - Security procedures

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Purpose**: Technical architecture reference
