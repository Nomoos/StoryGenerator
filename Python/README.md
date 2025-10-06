# Quick Start Guide - StoryGenerator

This guide will get you up and running with StoryGenerator in 15 minutes.

## Prerequisites

- Python 3.12+ installed
- OpenAI account with API access
- ElevenLabs account with API access (optional, for voice generation)
- ~$5-10 in API credits for testing

## Step-by-Step Setup

### 1. Clone and Setup (5 minutes)

```bash
# Clone the repository
git clone https://github.com/Nomoos/StoryGenerator.git
cd StoryGenerator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys (5 minutes)

⚠️ **CRITICAL**: Never commit API keys to Git!

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your favorite editor
nano .env  # or vim, code, etc.
```

Add your API keys to `.env`:
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
ELEVENLABS_API_KEY=sk_your-actual-key-here
```

### 3. Verify Installation (2 minutes)

```bash
# Test Python can import modules
python -c "from Generators.GStoryIdeas import StoryIdeasGenerator; print('✓ Installation verified')"

# Test environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ API keys loaded' if os.getenv('OPENAI_API_KEY') else '✗ Missing API key')"
```

### 4. Generate Your First Story (3 minutes)

Create a test script `quick_test.py`:

```python
from Generators.GStoryIdeas import StoryIdeasGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Generate story ideas
generator = StoryIdeasGenerator()

print("🎯 Generating story ideas...")
ideas = generator.generate_ideas(
    topic="falling for someone who gives mixed signals",
    count=2,
    tone="awkward, romantic, relatable",
    theme="first love, quiet sadness"
)

print(f"\n✅ Generated {len(ideas)} story ideas:\n")
for i, idea in enumerate(ideas, 1):
    print(f"{i}. {idea.story_title}")
    print(f"   Overall potential: {idea.potencial['overall']}/100")
    print(f"   Best platform: YouTube ({idea.potencial['platforms']['youtube']}/100)\n")
```

Run it:
```bash
python quick_test.py
```

Expected output:
```
🎯 Generating story ideas...

✅ Generated 2 story ideas:

1. I fell for my best friend who kept giving me mixed signals...
   Overall potential: 78/100
   Best platform: YouTube (85/100)

2. He said he liked me but wouldn't commit — here's what I learned
   Overall potential: 75/100
   Best platform: YouTube (82/100)
```

## Next Steps

### Generate a Complete Story

```python
from Generators.GStoryIdeas import StoryIdeasGenerator
from Generators.GScript import ScriptGenerator
from Models.StoryIdea import StoryIdea
from dotenv import load_dotenv

load_dotenv()

# 1. Generate ideas
idea_gen = StoryIdeasGenerator()
ideas = idea_gen.generate_ideas(
    topic="your topic here",
    count=1
)

# 2. Generate script from first idea
script_gen = ScriptGenerator()
script_gen.generate_from_storyidea(ideas[0])

print(f"✅ Script saved to: Stories/1_Scripts/{ideas[0].story_title}/")
```

### Understanding the Directory Structure

After generation, you'll see:

```
Stories/
├── 0_Ideas/              # Generated story ideas (JSON)
│   └── Your_Story_Title.json
├── 1_Scripts/            # Initial scripts
│   └── Your_Story_Title/
│       ├── Idea.json
│       └── Script.txt
├── 2_Revised/            # Revised scripts
└── 3_VoiceOver/          # Generated audio files
```

### Full Pipeline Example

```python
from dotenv import load_dotenv
from Generators.GStoryIdeas import StoryIdeasGenerator
from Generators.GScript import ScriptGenerator
from Generators.GRevise import RevisedScriptGenerator
from Generators.GEnhanceScript import EnhanceScriptGenerator
from Generators.GVoice import VoiceMaker

load_dotenv()

# 1. Generate idea
print("1️⃣ Generating idea...")
idea_gen = StoryIdeasGenerator()
ideas = idea_gen.generate_ideas(topic="your topic", count=1)
idea = ideas[0]
print(f"✓ Created: {idea.story_title}")

# 2. Generate initial script
print("\n2️⃣ Generating script...")
script_gen = ScriptGenerator()
script_gen.generate_from_storyidea(idea)
print("✓ Script generated")

# 3. Revise script
print("\n3️⃣ Revising script...")
reviser = RevisedScriptGenerator()
reviser.Revise(idea)
print("✓ Script revised")

# 4. Enhance with voice tags
print("\n4️⃣ Adding voice tags...")
enhancer = EnhanceScriptGenerator()
from Tools.Utils import sanitize_filename
enhancer.Enhance(sanitize_filename(idea.story_title))
print("✓ Voice tags added")

# 5. Generate voiceover (requires ElevenLabs API key)
print("\n5️⃣ Generating voiceover...")
voice_maker = VoiceMaker()
voice_maker.generate_audio()
print("✓ Voiceover generated")

print(f"\n🎉 Complete! Check: Stories/3_VoiceOver/{sanitize_filename(idea.story_title)}/")
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'dotenv'"

**Solution**:
```bash
pip install python-dotenv
```

### Issue: "OPENAI_API_KEY not found"

**Solution**:
1. Verify `.env` file exists in project root
2. Check `.env` contains: `OPENAI_API_KEY=your_key_here`
3. Ensure you called `load_dotenv()` in your code
4. Try absolute path: `load_dotenv('/path/to/StoryGenerator/.env')`

### Issue: "Rate limit exceeded"

**Solution**:
- Wait a few minutes before retrying
- Check your OpenAI usage dashboard
- Consider upgrading your API tier
- Implement retry logic (see RESEARCH_AND_IMPROVEMENTS.md)

### Issue: "Stories folder not created"

**Solution**:
```bash
mkdir -p Stories/{0_Ideas,1_Scripts,2_Revised,3_VoiceOver}
```

### Issue: Import errors on Windows

**Solution**:
Make sure you're in the project root directory:
```bash
cd StoryGenerator
python quick_test.py
```

## Understanding Costs

Approximate costs per story (as of January 2025):

| Step | Service | Approx. Cost |
|------|---------|--------------|
| Idea Generation | OpenAI (GPT-4o-mini) | $0.001 - $0.002 |
| Script Writing | OpenAI (GPT-4o-mini) | $0.002 - $0.005 |
| Script Revision | OpenAI (GPT-4o-mini) | $0.002 - $0.005 |
| Voice Tags | OpenAI (GPT-4o-mini) | $0.001 - $0.002 |
| Voiceover | ElevenLabs | $0.05 - $0.15 |
| **Total per story** | | **$0.06 - $0.17** |

💡 **Tip**: Start with just idea and script generation to test without voice costs.

## Best Practices

### 1. Start Small
```python
# Generate 1-2 ideas first
ideas = generator.generate_ideas(topic="test", count=2)
```

### 2. Check Outputs Between Steps
```bash
# After each generation, check the output
cat Stories/1_Scripts/Your_Story/Script.txt
```

### 3. Use Version Control
```bash
# Commit after successful generations
git add .
git commit -m "Generated story: Your Title"
```

### 4. Monitor API Usage
- OpenAI: https://platform.openai.com/usage
- ElevenLabs: https://elevenlabs.io/app/usage

## What to Do Next

1. **Read the full README**: [README.md](README.md)
2. **Review improvements**: [RESEARCH_AND_IMPROVEMENTS.md](RESEARCH_AND_IMPROVEMENTS.md)
3. **Check security**: [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md)
4. **Experiment with parameters**: Try different topics, tones, and themes
5. **Customize prompts**: Edit generator files to match your style

## Getting Help

- **Documentation**: Check README.md and other .md files
- **Issues**: Open a GitHub issue
- **Logs**: Check console output for error messages
- **API Docs**: 
  - [OpenAI API](https://platform.openai.com/docs)
  - [ElevenLabs API](https://elevenlabs.io/docs)

## Tips for Great Stories

1. **Be Specific with Topics**
   ```python
   # ✗ Too broad
   topic = "relationships"
   
   # ✓ Better
   topic = "falling for someone who gives mixed signals"
   ```

2. **Mix Tones**
   ```python
   # ✓ More engaging
   tone = "awkward, romantic, heartwarming"
   ```

3. **Target Your Audience**
   ```python
   # Adjust narrator gender and theme based on target demographic
   # The model uses this to optimize viral potential scores
   ```

4. **Review and Iterate**
   - Don't use the first generation blindly
   - Read through scripts and adjust
   - Regenerate if needed

## Success! 🎉

You should now have:
- ✅ Working environment
- ✅ Configured API keys
- ✅ Generated your first story ideas
- ✅ Understanding of the pipeline

Ready to create viral stories! 🚀

---

**Need more help?** Check the full [README.md](README.md) or open an issue on GitHub.
