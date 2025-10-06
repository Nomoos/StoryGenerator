# AI Video Pipeline - Detailed Component Breakdown

This document provides a comprehensive breakdown of all pipeline components, their current implementation status, requirements, and planned features.

## 📊 Pipeline Overview

```
Story Idea → Script Generation → Script Revision → Voice Synthesis
     ↓             ↓                   ↓                ↓
 [Metadata]   [GPT-4o-mini]    [GPT-4o-mini]    [ElevenLabs]
     ↓             ↓                   ↓                ↓
     └─────────────┴───────────────────┴────────────────┘
                            ↓
                    ASR & Alignment
                       [WhisperX]
                            ↓
                    ┌───────┴───────┐
                    ↓               ↓
            Vision Guidance    Keyframe Gen
            [LLaVA/Phi-3]        [SDXL]
                    ↓               ↓
                    └───────┬───────┘
                            ↓
                    Video Synthesis
                  [LTX/SVD/AnimateDiff]
                            ↓
                    Post-Production
                  [FFmpeg + Subtitles]
                            ↓
                    Final Video Output
```

## 🔧 Component Details

---

## 1. Environment & Model Setup

### Status: 🔄 Partial Implementation

### Current State
- ✅ Python environment with basic dependencies
- ✅ OpenAI API integration
- ✅ ElevenLabs API integration
- ✅ WhisperX setup for ASR
- ⚠️ No GPU optimization configuration
- ⚠️ No model caching strategy
- ⚠️ API keys hardcoded (security issue)

### Requirements
- [ ] CUDA environment setup guide
- [ ] Model download and caching system
- [ ] Environment variable configuration
- [ ] Docker container (optional)
- [ ] Requirements freezing by component
- [ ] GPU memory management
- [ ] API key management system

### Subtasks
1. Create environment setup script
2. Implement model caching (HuggingFace cache)
3. Add GPU detection and optimization
4. Create `.env.example` for API keys
5. Document system requirements (RAM, VRAM, disk)
6. Add model download verification

### Files to Create/Modify
- `setup.py` or `pyproject.toml`
- `.env.example`
- `config.py` for centralized configuration
- `requirements/` directory with split requirements
- `scripts/setup_environment.sh`

---

## 2. ASR Module (Transcription to Text & SRT)

### Status: ✅ Implemented (WhisperX) / 🔄 Enhancement Needed

### Current Implementation
- **File**: `Generators/GTitles.py`
- **Model**: WhisperX large-v2
- **Features**:
  - Word-level timestamp alignment
  - Script-to-audio synchronization
  - SRT file generation
  - Mismatch detection and estimation

### Current Workflow
```python
class TitleGenerator:
    def __init__(self, model_size="large-v2")
    def generate_titles()  # Main entry point
    def align_script_to_word_level_srt()  # Core alignment
    def _normalize_text()  # Text preprocessing
    def _export_word_srt()  # SRT generation
```

### Enhancement Requirements
- [ ] Upgrade to faster-whisper large-v3
- [ ] Add multi-language support
- [ ] Implement confidence scoring
- [ ] Add speaker diarization (if multiple voices)
- [ ] Optimize batch processing
- [ ] Add error recovery for poor audio quality

### Subtasks
1. Test faster-whisper large-v3 performance
2. Implement language detection
3. Add quality metrics (WER - Word Error Rate)
4. Create fallback strategies for alignment failures
5. Add progress callbacks for long audio files
6. Implement parallel processing for multiple files

### Performance Targets
- Transcription speed: >5x real-time
- Word-level accuracy: >95%
- Timestamp precision: ±50ms

### Files to Modify
- `Generators/GTitles.py`
- Add `Generators/GASR.py` (new dedicated ASR module)
- Add test files in `tests/test_asr.py`

---

## 3. LLM Content & Shotlist Generation

### Status: ✅ Basic Implementation / 🔄 Enhancement Needed

### Current Implementation

#### 3a. Script Generation
- **File**: `Generators/GScript.py`
- **Model**: GPT-4o-mini
- **Features**:
  - Story idea to script conversion
  - ~360 word target length
  - Emotional hook optimization
  - Conversational tone

#### 3b. Script Revision
- **File**: `Generators/GRevise.py`
- **Model**: GPT-4o-mini
- **Features**:
  - Voice-optimized rewrites
  - Awkward phrasing removal
  - Natural rhythm enhancement

### Enhancement Requirements
- [ ] Add shotlist generation capability
- [ ] Scene breakdown from script
- [ ] Visual cue extraction
- [ ] Emotional beat analysis
- [ ] Alternative LLM support (Qwen2.5, Llama-3.1)
- [ ] Token usage optimization
- [ ] Response caching

### Shotlist Generation Specification

**Input**: Revised script text  
**Output**: JSON structure with:
```json
{
  "scenes": [
    {
      "scene_id": 1,
      "duration_estimate": 5.2,
      "script_segment": "Walking down the hallway...",
      "visual_description": "Young girl, sad expression, dimly lit school hallway",
      "camera_angle": "medium shot",
      "lighting": "moody, dim",
      "emotion": "sadness, isolation",
      "movement": "slow walking",
      "suggested_prompt": "a young girl looking down, sad expression..."
    }
  ]
}
```

### Subtasks
1. Design shotlist JSON schema
2. Create prompt engineering for scene breakdown
3. Implement Qwen2.5-14B-Instruct integration
4. Implement Llama-3.1-8B-Instruct integration
5. Add LLM selection configuration
6. Create scene duration estimation algorithm
7. Build prompt templates for different shot types
8. Add consistency validation between scenes

### Files to Create/Modify
- `Generators/GShotlist.py` (new)
- `Models/Shotlist.py` (new data model)
- `Generators/GScript.py` (enhance)
- `config/llm_prompts.py` (prompt templates)

---

## 4. Vision Guidance (Optional)

### Status: ❌ Not Implemented

### Purpose
- Validate visual consistency across scenes
- Provide composition guidance
- Analyze reference images
- Quality check generated keyframes

### Proposed Models
- **LLaVA-OneVision**: Multi-modal understanding
- **Phi-3.5-vision**: Lightweight vision-language model

### Requirements
- [ ] Model selection and testing
- [ ] Integration with shotlist generation
- [ ] Keyframe validation pipeline
- [ ] Composition scoring
- [ ] Style consistency checking
- [ ] Reference image analysis

### Use Cases

#### 4a. Pre-Generation Guidance
- Analyze reference images for style
- Extract visual themes
- Suggest composition improvements

#### 4b. Post-Generation Validation
- Check keyframe quality
- Verify scene consistency
- Detect visual errors
- Validate character appearance consistency

### Subtasks
1. Evaluate LLaVA-OneVision vs Phi-3.5-vision
2. Create vision model wrapper
3. Design validation prompts
4. Implement consistency scoring
5. Add reference image input support
6. Create visual quality metrics
7. Build feedback loop to keyframe generation

### Integration Points
```
Shotlist → Vision Guidance → Enhanced Prompts → SDXL
            ↓
Keyframes → Vision Validation → Quality Score → Accept/Reject
```

### Files to Create
- `Generators/GVision.py`
- `Models/VisionAnalysis.py`
- `Tools/VisionUtils.py`
- `tests/test_vision.py`

---

## 5. Keyframe Generation (SDXL)

### Status: ✅ Implemented (SDXL-based)

### Current Implementation
- ✅ SDXL base + refiner pipeline
- ✅ 1080x1920 resolution (9:16 aspect ratio)
- ✅ Style presets (8 professional styles)
- ✅ Negative prompts library
- ✅ GPU optimizations (attention/VAE slicing)
- ✅ Complete metadata tracking
- ✅ Keyframe data model
- ✅ Image processing utilities

### Previous Exploration
- Basic Stable Diffusion 1.5 testing (see `Generation/Manual/Animation.py`)
- Latent space interpolation
- Frame sequence generation

### Completed Requirements
- [x] Upgrade to SDXL for better quality
- [x] Integrate with shotlist generation
- [x] Add style preservation (8 style presets)
- [x] Optimize generation speed (attention slicing, VAE slicing)
- [x] Implement seed management for reproducibility
- [ ] Implement consistent character generation (IP-Adapter - future)
- [ ] Implement LoRA/ControlNet support (future)

### SDXL Integration Specification

#### Input
- Scene description from shotlist
- Style parameters
- Character descriptions
- Composition guides

#### Output
- High-resolution keyframes (1080x1920 - 9:16 aspect ratio)
- Consistent style across scenes (via style presets)
- Complete metadata (seed, parameters, prompt, timing)

#### Generation Pipeline
```python
class KeyframeGenerator:
    def __init__(self, model="stabilityai/stable-diffusion-xl-base-1.0")
    def generate_scene_keyframes(shotlist: Shotlist) -> List[Image]
    def ensure_character_consistency(reference_image, scene_prompt)
    def apply_style_preset(style_name: str)
    def batch_generate(scenes: List[Scene]) -> Dict[int, Image]
```

### Subtasks
1. ✅ Set up SDXL pipeline (base + refiner)
2. ✅ Create prompt engineering from shotlist
3. ⏳ Implement IP-Adapter for character consistency (future)
4. ⏳ Add ControlNet for composition control (future)
5. ✅ Create style presets (8 styles implemented)
6. ✅ Implement negative prompts library
7. ⏳ Add quality validation (future - vision guidance)
8. ✅ Optimize VRAM usage (attention/VAE slicing)
9. ✅ Implement batch processing
10. ✅ Add seed management for reproducibility

### Performance Targets
- Generation time: ~8-10s per keyframe (with refiner) ✅
- Resolution: 1080x1920 (9:16 vertical) ✅
- VRAM usage: ~12-14GB (with refiner), ~8-10GB (base only) ✅
- Consistency: Via style presets and seed control ✅

### Files Created
- ✅ `Python/Generators/GKeyframeGenerator.py` (upgraded to SDXL)
- ✅ `Python/Models/Keyframe.py`
- ✅ `config/sdxl_config.py`
- ✅ `prompts/negative_prompts.txt`
- ✅ `prompts/style_presets.json`
- ✅ `Python/Tools/ImageUtils.py`
- ✅ `tests/test_keyframes.py`
- ✅ `docs/SDXL_KEYFRAME_GUIDE.md`
- ✅ `examples/sdxl_keyframe_example.py`

---

## 6. Video Synthesis

### Status: ❌ Not Implemented

### Purpose
Animate keyframes into smooth video sequences synchronized with audio.

### Proposed Models
- **LTX-Video**: Fast, high-quality video generation
- **Stable Video Diffusion**: Motion-controlled animation
- **AnimateDiff**: Animation from static images

### Requirements
- [ ] Model evaluation and selection
- [ ] Keyframe-to-video pipeline
- [ ] Motion control integration
- [ ] Audio synchronization
- [ ] Temporal consistency
- [ ] Transition smoothness

### Video Synthesis Specification

#### Input
- Keyframes from SDXL
- Scene durations from shotlist
- Audio file with timing
- Motion hints/prompts

#### Output
- Video clips per scene
- Synchronized with audio timing
- Smooth transitions
- Consistent motion

#### Pipeline Options

**Option A: LTX-Video**
- Pros: Fast generation, good quality
- Cons: Less motion control

**Option B: Stable Video Diffusion**
- Pros: Excellent quality, motion control
- Cons: Slower, higher VRAM

**Option C: Keyframe Interpolation**
- Pros: Fast, low resource
- Cons: Limited animation, static feel

### Subtasks
1. Evaluate video generation models
2. Implement LTX-Video pipeline
3. Implement SVD pipeline
4. Create motion prompt engineering
5. Add temporal consistency validation
6. Implement audio-driven motion
7. Add transition effects
8. Optimize rendering speed
9. Implement quality controls
10. Add frame rate optimization

### Performance Targets
- Generation time: <30s per 5s clip
- Frame rate: 24-30 fps
- Resolution: Match keyframes
- Temporal consistency: High

### Files to Create
- `Generators/GVideo.py`
- `Models/VideoClip.py`
- `Tools/VideoUtils.py`
- `tests/test_video_synthesis.py`

---

## 7. Post-Production

### Status: 🔄 Basic Implementation (audio to video conversion)

### Current Implementation
- **File**: `Tools/Utils.py`
- **Function**: `convert_to_mp4()`
- **Features**:
  - MP3 to MP4 with static image
  - Basic FFmpeg integration

### Requirements
- [ ] Dynamic subtitle overlay
- [ ] Subtitle styling (fonts, colors, animations)
- [ ] Audio-video synchronization validation
- [ ] Multiple output formats
- [ ] Resolution options
- [ ] Watermark support
- [ ] Intro/outro clips
- [ ] Background music mixing

### Post-Production Pipeline

#### 7a. Subtitle Overlay
```python
class SubtitleOverlay:
    def apply_word_by_word_srt(video_path, srt_path, style)
    def apply_dynamic_styling(emotion_hints)
    def add_background_boxes()
    def animate_text_entrance()
```

**Subtitle Styles**:
- Word-by-word highlighting
- Emotion-based color changes
- Dynamic positioning
- Background boxes/shadows
- Text animations (fade, slide, bounce)

#### 7b. Final Assembly
```python
class VideoAssembler:
    def combine_clips(clips: List[VideoClip]) -> Video
    def add_audio_track(video, audio)
    def add_background_music(video, music_path, volume)
    def add_intro_outro(video, intro_path, outro_path)
    def export_formats(video, formats: List[str])
```

### Subtasks
1. Implement subtitle overlay with FFmpeg
2. Create subtitle style presets
3. Add dynamic text animations
4. Implement emotion-based styling
5. Add background music mixing
6. Create intro/outro template system
7. Implement watermark positioning
8. Add multi-format export
9. Create preview generation
10. Add quality presets (mobile, HD, 4K)

### FFmpeg Command Templates
```bash
# Subtitle overlay with styling
ffmpeg -i input.mp4 -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=24,Bold=1'" output.mp4

# Word-by-word with highlights
# (Complex, requires custom filter)

# Add background music
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.3[a1];[0:a][a1]amix=inputs=2[a]" -map 0:v -map "[a]" output.mp4
```

### Files to Create/Modify
- `Generators/GPostProduction.py`
- `Tools/FFmpegUtils.py`
- `config/subtitle_styles.json`
- `assets/intro_templates/`
- `tests/test_post_production.py`

---

## 8. Integration & One-Click Pipeline

### Status: ❌ Not Implemented

### Purpose
Orchestrate all pipeline components into a single automated workflow.

### Requirements
- [ ] Pipeline orchestration class
- [ ] Error handling and recovery
- [ ] Progress tracking
- [ ] Logging system
- [ ] Checkpointing (resume from failure)
- [ ] Parallel processing where possible
- [ ] Resource management
- [ ] Configuration management

### One-Click Pipeline Design

```python
class VideoPipeline:
    def __init__(self, config: PipelineConfig):
        self.story_generator = StoryIdeaGenerator()
        self.script_gen = ScriptGenerator()
        self.revise_gen = RevisedScriptGenerator()
        self.voice_maker = VoiceMaker()
        self.asr = TitleGenerator()
        self.shotlist_gen = ShotlistGenerator()
        self.vision_guide = VisionGuidance()  # optional
        self.keyframe_gen = KeyframeGenerator()
        self.video_synth = VideoSynthesizer()
        self.post_prod = PostProduction()
    
    def run_full_pipeline(self, story_idea: StoryIdea) -> str:
        """Returns path to final video"""
        # 1. Generate/load story idea
        # 2. Generate script
        # 3. Revise script
        # 4. Generate voiceover
        # 5. Generate subtitles
        # 6. Generate shotlist
        # 7. (Optional) Vision guidance
        # 8. Generate keyframes
        # 9. Synthesize video
        # 10. Post-production
        pass
    
    def run_from_checkpoint(self, checkpoint_path: str):
        """Resume from saved state"""
        pass
```

### Subtasks
1. Design pipeline configuration schema
2. Implement pipeline orchestrator
3. Add progress tracking with callbacks
4. Implement error handling per stage
5. Add checkpoint/resume capability
6. Create logging system
7. Add resource monitoring (GPU, RAM)
8. Implement parallel processing
9. Add pipeline visualization
10. Create CLI interface
11. Add web interface (optional)

### Configuration Example
```yaml
pipeline:
  stages:
    - story_idea: true
    - script_generation: true
    - script_revision: true
    - voice_synthesis: true
    - asr: true
    - shotlist: true
    - vision_guidance: false  # optional
    - keyframe_generation: true
    - video_synthesis: true
    - post_production: true
  
  models:
    llm: "gpt-4o-mini"
    voice: "elevenlabs_v3"
    asr: "whisperx-large-v2"
    vision: "llava-onevision"  # optional
    image: "sdxl"
    video: "ltx-video"
  
  output:
    format: "mp4"
    resolution: "1080x1920"
    fps: 30
    quality: "high"
```

### Files to Create
- `pipeline.py` (main orchestrator)
- `config/pipeline_config.yaml`
- `Models/PipelineConfig.py`
- `Tools/PipelineUtils.py`
- `cli.py` (command-line interface)
- `tests/test_pipeline.py`

---

## 9. C# Implementation

### Status: ❌ Not Planned Yet

### Purpose
Provide C# bindings/implementation for integration with .NET applications.

### Requirements
- [ ] Evaluate implementation approach
- [ ] C# wrapper for Python pipeline (Python.NET)
- [ ] Native C# implementation (ONNX models)
- [ ] REST API with C# client
- [ ] gRPC service with C# client

### Implementation Options

#### Option A: Python.NET Wrapper
**Pros**: Reuse Python code, quick setup  
**Cons**: Python runtime dependency

#### Option B: REST API
**Pros**: Language agnostic, scalable  
**Cons**: Network overhead, deployment complexity

#### Option C: Native C# with ONNX
**Pros**: No Python dependency, better performance  
**Cons**: Model conversion complexity, limited model support

### Subtasks (Pending Decision)
1. Evaluate C# integration requirements
2. Choose implementation approach
3. Create C# project structure
4. Implement model wrappers
5. Create C# API
6. Add NuGet package
7. Write C# documentation
8. Create C# examples

### Files to Create (if pursued)
- `csharp/` directory
- `csharp/StoryGenerator.sln`
- `csharp/StoryGenerator/Pipeline.cs`
- `csharp/README.md`

---

## 10. Documentation & Issue Tracking

### Status: 🔄 In Progress

### Current Documentation
- ✅ README.md (this file)
- ✅ PIPELINE.md (component breakdown)
- ⚠️ No API documentation
- ⚠️ No usage examples
- ⚠️ No troubleshooting guide

### Requirements
- [x] Project README
- [x] Pipeline architecture document
- [ ] API documentation
- [ ] Usage examples
- [ ] Troubleshooting guide
- [ ] Model comparison benchmarks
- [ ] Performance optimization guide
- [ ] Deployment guide

### Child Issues to Create

1. **Issue: Environment & Model Setup**
   - Labels: setup, infrastructure
   - Components: all models
   
2. **Issue: ASR Enhancement (faster-whisper v3)**
   - Labels: enhancement, asr
   - Components: GTitles.py

3. **Issue: Shotlist Generation**
   - Labels: feature, llm
   - Components: new GShotlist.py

4. **Issue: Vision Guidance Integration**
   - Labels: feature, vision, optional
   - Components: new GVision.py

5. **Issue: SDXL Keyframe Generation**
   - Labels: feature, image-generation
   - Components: new GKeyframes.py

6. **Issue: Video Synthesis (LTX/SVD)**
   - Labels: feature, video-generation
   - Components: new GVideo.py

7. **Issue: Post-Production Enhancement**
   - Labels: enhancement, post-production
   - Components: GPostProduction.py, FFmpegUtils.py

8. **Issue: Pipeline Integration**
   - Labels: integration, pipeline
   - Components: pipeline.py, cli.py

9. **Issue: C# Implementation Research**
   - Labels: research, c-sharp
   - Components: TBD

10. **Issue: Documentation Completion**
    - Labels: documentation
    - Components: docs/, examples/

### Documentation Structure
```
docs/
├── API.md                    # API reference
├── INSTALLATION.md           # Detailed setup
├── USAGE.md                  # Usage examples
├── TROUBLESHOOTING.md        # Common issues
├── MODELS.md                 # Model comparisons
├── PERFORMANCE.md            # Optimization guide
├── DEPLOYMENT.md             # Production deployment
├── CONTRIBUTING.md           # Contribution guidelines
└── CHANGELOG.md              # Version history

examples/
├── basic_pipeline.py
├── custom_shotlist.py
├── batch_processing.py
└── advanced_config.py
```

### Subtasks
1. Create issue templates
2. Document each generator class
3. Add docstrings to all functions
4. Create usage examples
5. Write troubleshooting guide
6. Benchmark model performance
7. Create deployment guide
8. Set up changelog
9. Create contribution guidelines

---

## 📊 Implementation Priority

### Phase 1: Foundation (Weeks 1-2)
1. ✅ Environment setup documentation
2. ✅ API key management
3. ⚠️ Shotlist generation
4. ⚠️ Enhanced ASR module

### Phase 2: Visual Generation (Weeks 3-5)
5. SDXL keyframe generation
6. Vision guidance (optional parallel track)
7. Style consistency system

### Phase 3: Video & Integration (Weeks 6-8)
8. Video synthesis (LTX-Video or SVD)
9. Post-production enhancements
10. Pipeline integration

### Phase 4: Polish & Extension (Weeks 9-10)
11. C# implementation research
12. Documentation completion
13. Performance optimization
14. Testing and validation

---

## 🧪 Testing Strategy

### Unit Tests
- Each generator class
- Utility functions
- Model wrappers

### Integration Tests
- Pipeline stages
- End-to-end workflow
- Error recovery

### Performance Tests
- Model inference speed
- Memory usage
- GPU utilization
- Pipeline throughput

### Quality Tests
- Output validation
- Consistency checks
- Visual quality metrics

---

## 📈 Success Metrics

### Technical Metrics
- Pipeline success rate: >95%
- Average generation time: <10 minutes per video
- VRAM usage: <16GB
- Output quality score: >8/10

### Content Metrics
- Script engagement potential
- Visual consistency score
- Audio quality (LUFS, clarity)
- Subtitle accuracy

---

## 🔄 Continuous Improvement

### Planned Enhancements
- Model fine-tuning for specific styles
- Multi-language support
- Real-time preview
- Cloud deployment
- API service
- Web interface
- Mobile app integration

---

## 📝 Notes

- All timestamps in this document are estimates
- Model selection may change based on performance testing
- C# implementation is low priority, pending user feedback
- Vision guidance is optional but recommended for quality

---

*Last Updated: 2025-10-06*
*Document Version: 1.0*
