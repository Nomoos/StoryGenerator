# Video Prompt Templates Documentation

## Overview

The `VideoPromptTemplates.cs` class provides specialized prompt templates for AI video generation, optimized based on analysis of successful viral short-form content (YouTube Shorts, TikTok, Reels).

## Research Foundation

These templates are based on comprehensive analysis of:

### Story Pattern Analysis
- **6 successful YouTube stories** analyzed for patterns
- **Average metrics**: 632 words, 67 sentences, 9.9 words/sentence
- **Hook analysis**: 6-16 words optimal length
- **Story arc**: Setup → Conflict → Escalation → Climax → Resolution (100% resolution rate)
- **Dialogue usage**: 83% of successful stories include dialogue
- **Emotional triggers**: angry, shocked, happy, heartbroken, relieved

### Subtitle Timing Analysis
- **Optimal duration**: 2-8 seconds per scene (average 2.5s)
- **Reading speed**: 2.0-3.5 words per second
- **Format**: 9:16 vertical (1080x1920)
- **Target audience**: Ages 10-30

### Viral Video Requirements
- **First 3 seconds critical** for viewer retention
- **Mobile-first** vertical composition
- **Emotional resonance** drives engagement
- **Clear resolution** provides satisfaction

## Template Categories

### 1. Cinematic Video Templates

**Purpose**: Professional, dramatic visual storytelling

**System Prompt**: `CinematicVideoSystem`
- Master cinematographer perspective
- Film-quality aesthetics
- Professional camera techniques
- Dramatic lighting and composition

**User Prompt**: `CinematicVideoUser`
```csharp
string prompt = VideoPromptTemplates.FormatCinematicVideoPrompt(
    sceneDescription: "A young woman reading a letter with tears in her eyes",
    emotion: "heartbreak",
    duration: 3.5f
);
```

**Use Cases**:
- High-quality dramatic scenes
- Emotional story peaks
- Professional-looking content
- Brand storytelling

### 2. Documentary Style Templates

**Purpose**: Realistic, authentic storytelling

**System Prompt**: `DocumentaryVideoSystem`
- Documentary filmmaker perspective
- Natural, unscripted feel
- Realistic environments
- Authentic emotions

**User Prompt**: `DocumentaryVideoUser`
```csharp
string prompt = VideoPromptTemplates.FormatDocumentaryVideoPrompt(
    sceneDescription: "Person working late at night in office",
    setting: "dimly lit office cubicle",
    mood: "exhausted but determined"
);
```

**Use Cases**:
- Real-life situations
- Behind-the-scenes content
- Personal stories
- Relatable moments

### 3. Emotional Storytelling Templates

**Purpose**: Maximizing emotional engagement

**System Prompt**: `EmotionalStoryVideoSystem`
- Psychology of engagement
- Emotional trigger optimization
- Visual metaphors for feelings
- Character-focused storytelling

**User Prompt**: `EmotionalStoryVideoUser`
```csharp
string prompt = VideoPromptTemplates.FormatEmotionalStoryPrompt(
    storyBeat: "Discovery of betrayal",
    primaryEmotion: "shocked",
    secondaryEmotions: "angry, hurt"
);
```

**Use Cases**:
- Story climax moments
- Character revelations
- Emotional turning points
- Viral potential scenes

### 4. Action and Dynamic Movement Templates

**Purpose**: High-energy, kinetic scenes

**System Prompt**: `ActionVideoSystem`
- Action cinematography specialist
- Dynamic camera movements
- Motion blur and speed effects
- High energy composition

**User Prompt**: `ActionVideoUser`
```csharp
string prompt = VideoPromptTemplates.FormatActionVideoPrompt(
    actionDescription: "Person running through crowded street",
    intensity: "high",
    cameraMovement: "tracking shot"
);
```

**Use Cases**:
- Chase scenes
- Fast-paced transitions
- Physical actions
- Energy-filled moments

### 5. Character Close-Up Templates

**Purpose**: Intimate emotional connection

**System Prompt**: `CharacterCloseUpSystem`
- Portrait cinematography
- Micro-expressions
- Emotional authenticity
- Viewer connection

**User Prompt**: `CharacterCloseUpUser`
```csharp
string prompt = VideoPromptTemplates.FormatCharacterCloseUpPrompt(
    characterDescription: "Young woman, early 20s",
    emotion: "relieved",
    lighting: "soft natural light"
);
```

**Use Cases**:
- Emotional peaks
- Reactions
- Dialogue delivery
- Character connection moments

### 6. Establishing Shot Templates

**Purpose**: Scene setting and context

**System Prompt**: `EstablishingShotSystem`
- Location scouting perspective
- Environmental storytelling
- Atmospheric conditions
- Spatial context

**User Prompt**: `EstablishingShotUser`
```csharp
string prompt = VideoPromptTemplates.FormatEstablishingShotPrompt(
    location: "High school hallway",
    timeOfDay: "early morning",
    atmosphere: "quiet, empty, lonely"
);
```

**Use Cases**:
- Scene openings
- Location changes
- Time transitions
- Mood setting

### 7. Transition Shot Templates

**Purpose**: Smooth story flow between scenes

**System Prompt**: `TransitionShotSystem`
- Video editing specialist
- Visual metaphors
- Match cuts
- Temporal progression

**User Prompt**: `TransitionShotUser`
```csharp
string prompt = VideoPromptTemplates.FormatTransitionShotPrompt(
    fromEmotion: "anger",
    toEmotion: "calm",
    transitionType: "dissolve"
);
```

**Use Cases**:
- Scene transitions
- Time passage
- Mood shifts
- Story flow

### 8. Hook Shot Templates (First 3 Seconds)

**Purpose**: Maximum viewer retention

**System Prompt**: `HookShotSystem`
- Social media expert
- Viewer retention optimization
- Based on 6-16 word hook analysis
- Curiosity gap creation

**User Prompt**: `HookShotUser`
```csharp
string prompt = VideoPromptTemplates.FormatHookShotPrompt(
    hookConcept: "My neighbor blocked my driveway",
    conflictElement: "car blocking driveway, frustrated person"
);
```

**Use Cases**:
- Video opening (0-3 seconds)
- Scroll-stopping content
- Immediate conflict presentation
- Attention capture

**Critical Success Factors**:
- Visual within first 3 seconds
- Shows conflict/intrigue immediately
- Creates curiosity gap
- Stops mid-scroll

### 9. Resolution Shot Templates

**Purpose**: Satisfying story conclusion

**System Prompt**: `ResolutionShotSystem`
- Storytelling conclusion expert
- Emotional catharsis
- Visual satisfaction
- 100% resolution requirement (from research)

**User Prompt**: `ResolutionShotUser`
```csharp
string prompt = VideoPromptTemplates.FormatResolutionShotPrompt(
    resolutionDescription: "Neighbors shaking hands and laughing",
    finalEmotion: "relieved",
    payoff: "conflict resolved, friendship formed"
);
```

**Use Cases**:
- Final scene
- Story conclusion
- Emotional payoff
- Viewer satisfaction

**Critical Requirements**:
- Clear conflict resolution
- Emotional satisfaction
- Memorable final image
- Sense of completion

## Advanced System Prompts

### Age-Appropriate Content Filter

**Purpose**: Ensure content is suitable for 10-30 demographic

**System Prompt**: `AgeAppropriateFilterSystem`
- Content moderation
- Age-appropriate filtering
- Inclusive representation
- Positive mental health

**Usage**:
```csharp
// Use as additional context when generating sensitive content
var systemPrompt = VideoPromptTemplates.AgeAppropriateFilterSystem;
var generator = new LLMContentGenerator(modelProvider, "gpt-4o", systemPrompt);
```

### Vertical Video Optimization

**Purpose**: Optimize for 9:16 mobile format

**System Prompt**: `VerticalVideoOptimizationSystem`
- Mobile-first design
- Portrait orientation
- Safe areas (top 8%, bottom 10%)
- Thumb-stopping hierarchy

**Usage**:
```csharp
// Use when generating any video prompts for TikTok/Reels/Shorts
var systemPrompt = VideoPromptTemplates.VerticalVideoOptimizationSystem;
```

### Viral Optimization

**Purpose**: Maximize engagement and share-ability

**System Prompt**: `ViralOptimizationSystem`
- Based on successful viral patterns
- Emotional triggers
- Story arc optimization
- Shareable moments

**Usage**:
```csharp
// Use when optimizing for maximum viral potential
var systemPrompt = VideoPromptTemplates.ViralOptimizationSystem;
```

## Best Practices

### Shot Duration Guidelines

Based on research analysis:

```csharp
// Optimal shot durations
const float HOOK_DURATION = 3.0f;        // First 3 seconds
const float MIN_SHOT_DURATION = 2.0f;    // Minimum per shot
const float MAX_SHOT_DURATION = 8.0f;    // Maximum per shot
const float AVERAGE_DURATION = 2.5f;     // Target average
```

### Story Arc Implementation

All shotlists should follow this structure:

1. **Hook** (0-3s): Immediate conflict/intrigue
2. **Setup** (3-10s): Context and characters
3. **Conflict** (10-25s): Problem escalation
4. **Climax** (25-35s): Turning point
5. **Resolution** (35-60s): Satisfying conclusion

### Emotional Progression

Use research-identified trigger words:

```csharp
var emotionalTriggers = new[]
{
    "shocked", "angry", "happy", "heartbroken", 
    "relieved", "curious", "confused", "hopeful"
};
```

### Visual Variety

Maintain engagement with varied shots:

- 30% close-ups (emotional moments)
- 40% medium shots (action/dialogue)
- 20% wide shots (context/establishing)
- 10% transition/creative shots

## Integration Examples

### Complete Video Generation Workflow

```csharp
using StoryGenerator.Core.LLM;

// 1. Generate hook shot (0-3 seconds)
var hookPrompt = VideoPromptTemplates.FormatHookShotPrompt(
    "My neighbor blocked my driveway",
    "frustrated person staring at blocked car"
);

// 2. Generate emotional story beats
var emotionalPrompt = VideoPromptTemplates.FormatEmotionalStoryPrompt(
    "Confrontation with neighbor",
    "angry",
    "frustrated, defensive"
);

// 3. Generate character close-ups
var closeUpPrompt = VideoPromptTemplates.FormatCharacterCloseUpPrompt(
    "Middle-aged neighbor, defensive posture",
    "annoyed",
    "harsh natural sunlight"
);

// 4. Generate resolution
var resolutionPrompt = VideoPromptTemplates.FormatResolutionShotPrompt(
    "Neighbors laughing and shaking hands",
    "relieved",
    "mutual understanding reached"
);
```

### Using with LLMContentGenerator

```csharp
using StoryGenerator.Core.LLM;

var generator = new LLMContentGenerator(modelProvider, "gpt-4o");

// Generate cinematic video description
var cinematicResult = await generator.GenerateAsync(
    systemPrompt: VideoPromptTemplates.CinematicVideoSystem,
    userPrompt: VideoPromptTemplates.FormatCinematicVideoPrompt(
        "Emotional reunion at airport",
        "joy",
        4.5f
    ),
    temperature: 0.7f
);

// Generate with viral optimization
var viralResult = await generator.GenerateAsync(
    systemPrompt: VideoPromptTemplates.ViralOptimizationSystem,
    userPrompt: VideoPromptTemplates.FormatHookShotPrompt(
        "She said yes to the prenup, then saw my bank account",
        "shocked woman staring at phone screen"
    ),
    temperature: 0.8f
);
```

## Performance Tips

### Temperature Settings

```csharp
// Recommended temperature values
const float CREATIVE_TEMP = 0.8f;      // Creative variations
const float BALANCED_TEMP = 0.7f;      // Balanced creativity/consistency
const float PRECISE_TEMP = 0.6f;       // Precise, technical descriptions
const float STRUCTURED_TEMP = 0.5f;    // Structured outputs (JSON)
```

### Template Selection Guide

| Content Type | Recommended Template | Priority Metrics |
|-------------|---------------------|------------------|
| Drama/Story | EmotionalStoryVideo | Emotional engagement |
| Real-life | DocumentaryVideo | Authenticity |
| High-quality | CinematicVideo | Visual quality |
| Fast-paced | ActionVideo | Energy/movement |
| Character focus | CharacterCloseUp | Emotional connection |
| Opening | HookShot | Retention (first 3s) |
| Closing | ResolutionShot | Satisfaction |

## Testing and Validation

### Quality Checklist

- [ ] Hook shot (0-3s) immediately shows conflict
- [ ] Story follows arc: Setup → Conflict → Escalation → Climax → Resolution
- [ ] Shot durations: 2-8 seconds (average 2.5s)
- [ ] Emotional progression with trigger words
- [ ] Character close-ups at emotional peaks
- [ ] Visual variety maintained
- [ ] Resolution provides closure
- [ ] Optimized for 9:16 vertical format
- [ ] Age-appropriate for 10-30 demographic
- [ ] Prompts include technical details (camera, lighting, composition)

### Success Metrics

Based on research analysis:

- **Retention Rate**: >70% watch through (hook critical)
- **Engagement Rate**: >5% (likes, comments, shares)
- **Completion Rate**: >80% (resolution requirement)
- **Share Rate**: >2% (emotional satisfaction)

## Future Enhancements

Potential additions based on ongoing research:

1. **Platform-specific templates** (TikTok vs Reels vs Shorts)
2. **Genre-specific templates** (comedy, horror, inspirational)
3. **Multi-language optimization**
4. **Trend integration** (current viral patterns)
5. **A/B testing variations**
6. **Performance analytics integration**

## References

- `research/story_analysis/story_patterns_analysis.json`
- `research/subtitle_analysis/RESEARCH_SUMMARY.md`
- `research/VIRAL_VIDEO_REQUIREMENTS.md`
- `research/story_analysis/story_patterns_report.md`

## Support

For questions or contributions:
- Review research files in `/research` directory
- Check existing usage in `LLMContentGenerator.cs`
- See `PromptTemplates.cs` for base templates
- Refer to test examples in `StoryGenerator.Tests`
