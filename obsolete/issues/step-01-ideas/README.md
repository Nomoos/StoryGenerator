# Step 01: Ideas → Topics → Titles

## Purpose

Generate story ideas, cluster them into topics, and create compelling titles. This is the first content-generation step that produces the raw material for scripts. The step:
- Generates 20+ raw ideas per audience segment using local LLM
- Clusters similar ideas into coherent topics
- Creates 5-10 title variants per idea
- Provides foundation for viral score calculation (Step 02)

## Status

**Implementation:** ✅ Complete (Python + C# pipeline stages)  
**Testing:** ⚠️ Needs Testing (manual verification needed)  
**Documentation:** ✅ Complete (this README + issue.md)

## Dependencies

**Requires:**
- **Previous steps:** None (or optionally Step 00 for research validation)
- **API services:** 
  - OpenAI GPT-4 (for C# implementation)
  - Local LLM via Ollama (for Python implementation)
- **Models/Libraries:**
  - Ollama with Qwen2.5 or Llama3.1 (Python)
  - OpenAI SDK (C#)

**Outputs used by:**
- Step 02: Viral Score (titles are scored)
- Step 03: Raw Script (selected ideas become scripts)

## Implementation

### Code Location

**Python Implementation:**
- Primary: `core/pipeline/idea_generation.py` (11,413 bytes)
- Topic clustering: `core/pipeline/topic_clustering.py` (6,717 bytes)
- Title generation: `core/pipeline/title_generation.py` (6,447 bytes)

**C# Implementation:**
- Primary: `src/CSharp/StoryGenerator.Pipeline/Stages/LLMIdeaGenerationStage.cs`
- Processing: `src/CSharp/StoryGenerator.Pipeline/Stages/IdeaProcessingStages.cs`
- Finalization: `src/CSharp/StoryGenerator.Pipeline/Stages/IdeaFinalizationStages.cs`
- Models: `src/CSharp/StoryGenerator.Core/Models/StoryIdea.cs`
- Generators: `src/CSharp/StoryGenerator.Generators/IdeaGenerator.cs`

### Key Classes/Functions

**Python:**
- `generate_ideas()` - Generate raw ideas using LLM
- `cluster_topics()` - Group similar ideas
- `generate_titles()` - Create title variants

**C#:**
- `LLMIdeaGenerationStage` - Main idea generation stage
- `IdeaClusteringStage` - Topic clustering
- `TitleGenerationStage` - Title variant creation
- `IdeaGenerator` - Core idea generation logic
- `StoryIdea` - Data model for ideas

## Input/Output

### Input Format

**Minimal Input (Fresh Start):**
```json
{
  "segment": "women",
  "age_group": "18-23",
  "count": 20,
  "theme": "emotional stories",
  "tone": "inspirational"
}
```

**Optional Input (From Step 00 Research):**
- Research insights
- Trending topics
- Competitor analysis

**Location:** Configuration or API call

### Output Format

**Ideas Output:**

**Location:** `src/Generator/ideas/{segment}/{age}/YYYYMMDD_ideas.md` or `.json`

**Format (Markdown):**
```markdown
# Story Ideas - Women 18-23 - 2025-10-10

## Idea 1: The Lost Letter
A woman discovers a letter from her grandmother...

## Idea 2: Coffee Shop Connection
Two strangers meet at a coffee shop...

[... 18 more ideas ...]
```

**Format (JSON):**
```json
{
  "generation_date": "2025-10-10",
  "segment": "women",
  "age_group": "18-23",
  "ideas": [
    {
      "id": "idea_001",
      "title": "The Lost Letter",
      "summary": "A woman discovers a letter from her grandmother...",
      "theme": "family",
      "emotional_tone": "nostalgic"
    }
  ]
}
```

**Topics Output:**

**Location:** `src/Generator/topics/{segment}/{age}/YYYYMMDD_topics.json`

**Format:**
```json
{
  "topics": [
    {
      "topic_id": "topic_001",
      "name": "Family Connections",
      "ideas": ["idea_001", "idea_005", "idea_012"],
      "keywords": ["family", "grandmother", "heritage"]
    }
  ]
}
```

**Titles Output:**

**Location:** `src/Generator/titles/{segment}/{age}/YYYYMMDD_titles.json`

**Format:**
```json
{
  "titles": [
    {
      "idea_id": "idea_001",
      "variants": [
        "The Lost Letter That Changed Everything",
        "A Grandmother's Secret Letter",
        "The Letter I Never Knew Existed",
        "Discovering My Family's Hidden Past",
        "The Day I Found Grandma's Letter"
      ]
    }
  ]
}
```

**Artifacts Created:**
- `YYYYMMDD_ideas.md` or `.json` - Raw ideas
- `YYYYMMDD_topics.json` - Clustered topics
- `YYYYMMDD_titles.json` - Title variants

## Usage

### CLI Command

```bash
# Generate ideas for a specific segment
dotnet run --project src/CSharp/StoryGenerator.CLI -- ideas generate \
  --segment women \
  --age 18-23 \
  --count 20

# Or use Python
python3 core/pipeline/idea_generation.py \
  --segment women \
  --age 18-23 \
  --count 20 \
  --output src/Generator/ideas/women/18-23/
```

### Programmatic Usage

**C# Example:**
```csharp
// Using pipeline stage
var ideaStage = new LLMIdeaGenerationStage(logger, config, ideaGenerator);
var input = new IdeaGenerationInput
{
    Segment = "women",
    AgeGroup = "18-23",
    Count = 20,
    Theme = "emotional stories"
};
var output = await ideaStage.ExecuteAsync(input);

// Using generator directly
var generator = new IdeaGenerator(openAiProvider, logger, config);
var ideas = await generator.GenerateIdeasAsync(20, "women", "18-23");
```

**Python Example:**
```python
from core.pipeline.idea_generation import generate_ideas
from core.pipeline.topic_clustering import cluster_topics
from core.pipeline.title_generation import generate_titles

# Generate ideas
ideas = generate_ideas(
    segment="women",
    age_group="18-23",
    count=20,
    theme="emotional stories"
)

# Cluster into topics
topics = cluster_topics(ideas)

# Generate title variants
titles = generate_titles(ideas, variants_per_idea=5)
```

### Configuration

**Required Settings:**
```json
{
  "Generation": {
    "Story": {
      "Count": 20,
      "Tone": "emotional",
      "Theme": "inspirational",
      "MinLength": 50,
      "MaxLength": 200
    }
  },
  "OpenAI": {
    "Model": "gpt-4",
    "Temperature": 0.7,
    "MaxTokens": 2000
  }
}
```

**Optional Settings:**
- `TopicsPerSegment` - Number of topic clusters (default: 3-5)
- `TitlesPerIdea` - Title variants per idea (default: 5)
- `UseLocalLLM` - Use Ollama instead of OpenAI (default: false)

## Testing

### Manual Test

```bash
# 1. Set up configuration
# Edit src/CSharp/StoryGenerator.CLI/appsettings.json
# Add OpenAI API key to environment: export OPENAI_API_KEY=sk-...

# 2. Generate ideas for test segment
dotnet run --project src/CSharp/StoryGenerator.CLI -- ideas generate \
  --segment women \
  --age 18-23 \
  --count 5

# 3. Verify output
ls src/Generator/ideas/women/18-23/
# Should see: YYYYMMDD_ideas.json

cat src/Generator/ideas/women/18-23/YYYYMMDD_ideas.json
# Should see: 5 story ideas in JSON format

# 4. Generate topics
dotnet run --project src/CSharp/StoryGenerator.CLI -- topics cluster \
  --input src/Generator/ideas/women/18-23/YYYYMMDD_ideas.json

# 5. Generate titles
dotnet run --project src/CSharp/StoryGenerator.CLI -- titles generate \
  --input src/Generator/ideas/women/18-23/YYYYMMDD_ideas.json \
  --variants 5

# 6. Verify final output
ls src/Generator/titles/women/18-23/
# Should see: YYYYMMDD_titles.json
```

### Automated Tests

**Test Files:**
- `src/CSharp/StoryGenerator.Tests/Generators/IdeaGeneratorTests.cs`
- `src/CSharp/StoryGenerator.Tests/Pipeline/IdeaGenerationTests.cs`

**Run Tests:**
```bash
# C# tests
dotnet test src/CSharp/StoryGenerator.Tests \
  --filter "Category=IdeaGeneration"

# Python tests (if available)
pytest tests/test_idea_generation.py
```

## Error Handling

**Common Errors:**

1. **OpenAI API Error: Rate Limit Exceeded**
   - Cause: Too many API calls in short time
   - Solution: Add retry with exponential backoff, reduce count, use local LLM

2. **OpenAI API Error: Invalid API Key**
   - Cause: Missing or incorrect API key
   - Solution: Set `OPENAI_API_KEY` environment variable

3. **Insufficient Ideas Generated**
   - Cause: LLM returned fewer ideas than requested
   - Solution: Retry with different prompt or lower count

4. **Invalid JSON Output**
   - Cause: LLM output not properly formatted
   - Solution: Validate and parse with error handling, retry

5. **Topic Clustering Failed**
   - Cause: Too few ideas or all ideas too dissimilar
   - Solution: Generate more ideas or adjust clustering parameters

**Retry Policy:** 
- Automatic retry up to 3 times with exponential backoff
- Implemented in `RetryService` using Polly library

**Graceful Degradation:** 
- Fall back to local LLM if OpenAI unavailable
- Generate fewer ideas if API quota exhausted
- Skip clustering if insufficient ideas

## Performance

**Expected Runtime:**
- Idea generation: 30-90 seconds for 20 ideas (depends on API/LLM speed)
- Topic clustering: 1-5 seconds (local computation)
- Title generation: 10-30 seconds for 5 titles per idea

**Total for 20 ideas → titles:** 2-5 minutes

**Resource Requirements:**
- **CPU:** Minimal (API calls)
- **Memory:** < 500 MB
- **GPU:** Not required (unless using local LLM)
- **API Calls:**
  - OpenAI: ~2-5 calls (idea generation + title generation)
  - Cost: ~$0.10-0.50 per segment (GPT-4)

**Optimization Tips:**
- Use GPT-3.5-turbo for faster/cheaper generation (lower quality)
- Batch API calls where possible
- Cache results to avoid regeneration
- Use local LLM for development/testing (free)

## Related Documentation

- [Main Issue](./issue.md) - Detailed requirements and checklist (14,755 bytes)
- [Pipeline Guide](../../src/CSharp/PIPELINE_GUIDE.md) - Stage 1: Story Idea Generation
- [Quick Start](../../issues/QUICKSTART.md) - Getting started guide
- [OpenAI Provider](../../src/CSharp/StoryGenerator.Providers/OpenAIProvider.cs) - API integration

## Examples

### Example 1: Generate Ideas for Young Women

**Input:**
```json
{
  "segment": "women",
  "age_group": "18-23",
  "count": 3,
  "theme": "personal growth",
  "tone": "inspirational"
}
```

**Command:**
```bash
dotnet run --project src/CSharp/StoryGenerator.CLI -- ideas generate \
  --segment women \
  --age 18-23 \
  --count 3 \
  --theme "personal growth"
```

**Expected Output (ideas.json):**
```json
{
  "generation_date": "2025-10-10T14:30:00Z",
  "segment": "women",
  "age_group": "18-23",
  "theme": "personal growth",
  "ideas": [
    {
      "id": "idea_001",
      "title": "The Interview",
      "summary": "A young woman overcomes her fear of public speaking to nail her dream job interview.",
      "theme": "confidence",
      "emotional_tone": "triumphant",
      "keywords": ["career", "confidence", "growth"]
    },
    {
      "id": "idea_002",
      "title": "Solo Trip",
      "summary": "She takes her first solo trip abroad and discovers her independence.",
      "theme": "self-discovery",
      "emotional_tone": "adventurous",
      "keywords": ["travel", "independence", "courage"]
    },
    {
      "id": "idea_003",
      "title": "The Art Class",
      "summary": "She enrolls in an art class despite having no experience and finds her passion.",
      "theme": "creativity",
      "emotional_tone": "joyful",
      "keywords": ["art", "passion", "trying new things"]
    }
  ]
}
```

### Example 2: Generate Titles for Existing Ideas

**Input:** `ideas.json` from Example 1

**Command:**
```bash
dotnet run --project src/CSharp/StoryGenerator.CLI -- titles generate \
  --input src/Generator/ideas/women/18-23/20251010_ideas.json \
  --variants 5
```

**Expected Output (titles.json):**
```json
{
  "titles": [
    {
      "idea_id": "idea_001",
      "original": "The Interview",
      "variants": [
        "The Interview That Changed Everything",
        "How I Conquered My Fear of Public Speaking",
        "From Nervous Wreck to Dream Job",
        "The Day I Faced My Biggest Fear",
        "My Life-Changing Interview Story"
      ]
    }
  ]
}
```

## Troubleshooting

**Q: Ideas are not age-appropriate for the target segment**  
A: Adjust the prompt in configuration to emphasize age-appropriateness. Review generated ideas manually and regenerate if needed.

**Q: Ideas are too similar to each other**  
A: Increase temperature in OpenAI config (0.8-0.9), or use different prompt seeds. Topic clustering should help identify duplicates.

**Q: Title variants are all too similar**  
A: Increase temperature, request more diverse styles in prompt, or use different phrasing patterns.

**Q: Generation is too slow**  
A: 
1. Use GPT-3.5-turbo instead of GPT-4 (faster, cheaper)
2. Reduce count of ideas generated
3. Use local LLM for development (faster, but may need quality tuning)

**Q: OpenAI API costs are too high**  
A:
1. Use GPT-3.5-turbo (~10x cheaper than GPT-4)
2. Use local LLM (Ollama with Qwen2.5) - free but requires local compute
3. Cache and reuse ideas where possible

**Q: Local LLM (Ollama) produces poor quality ideas**  
A:
1. Try different models (Llama3.1 vs Qwen2.5)
2. Adjust temperature and prompt engineering
3. Generate more ideas and filter manually
4. Use OpenAI for production, local LLM for development only

## Changelog

- **2025-10-10**: Added comprehensive README documentation
- **2024**: Initial Python and C# implementations
- **2024**: Integrated with OpenAI GPT-4 API
- **2024**: Added topic clustering and title generation

---

**Last Updated:** 2025-10-10  
**Maintained By:** StoryGenerator Development Team  
**Status:** ✅ Implemented, ⚠️ Needs testing with live data
