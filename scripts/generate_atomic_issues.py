#!/usr/bin/env python3
"""
Generate atomic issue files for StoryGenerator pipeline.

Creates 62 atomic, parallelizable issue files based on templates.
"""

from pathlib import Path
from typing import Dict, List

# Define all 62 atomic tasks
ATOMIC_TASKS = [
    # Setup & Configuration (P0)
    {"id": "00-setup-01-repo-structure", "priority": "P0", "effort": "1-2", "title": "Setup: Repository Folder Structure"},
    {"id": "00-setup-02-config-files", "priority": "P0", "effort": "2-3", "title": "Setup: Configuration Files (YAML)"},
    {"id": "00-setup-03-python-env", "priority": "P0", "effort": "1-2", "title": "Setup: Python Environment", "requires": ["00-setup-02"]},
    {"id": "00-setup-04-csharp-projects", "priority": "P0", "effort": "2-3", "title": "Setup: C# Project Structure", "requires": ["00-setup-01"]},
    
    # Research Prototypes (P0/P1)
    {"id": "01-research-01-ollama-client", "priority": "P0", "effort": "4-6", "title": "Research: Ollama LLM Client", "requires": ["00-setup-03"]},
    {"id": "01-research-02-whisper-client", "priority": "P0", "effort": "4-6", "title": "Research: Whisper ASR Client", "requires": ["00-setup-03"]},
    {"id": "01-research-03-ffmpeg-client", "priority": "P0", "effort": "4-6", "title": "Research: FFmpeg Media Client", "requires": ["00-setup-03"]},
    {"id": "01-research-04-sdxl-client", "priority": "P1", "effort": "6-8", "title": "Research: SDXL Image Client", "requires": ["00-setup-03"]},
    {"id": "01-research-05-ltx-client", "priority": "P1", "effort": "6-8", "title": "Research: LTX Video Client", "requires": ["00-setup-03"]},
    {"id": "01-research-06-csharp-ollama", "priority": "P1", "effort": "4-6", "title": "Research: C# Ollama Client", "requires": ["00-setup-04", "01-research-01"]},
    {"id": "01-research-07-csharp-whisper", "priority": "P1", "effort": "4-6", "title": "Research: C# Whisper Client", "requires": ["00-setup-04", "01-research-02"]},
    {"id": "01-research-08-csharp-ffmpeg", "priority": "P1", "effort": "4-6", "title": "Research: C# FFmpeg Client", "requires": ["00-setup-04", "01-research-03"]},
    
    # Content Collection (P0/P1)
    {"id": "02-content-01-reddit-scraper", "priority": "P0", "effort": "4-6", "title": "Content: Reddit Story Scraper", "requires": ["00-setup-01", "00-setup-02"]},
    {"id": "02-content-02-alt-sources", "priority": "P1", "effort": "6-8", "title": "Content: Alternative Sources (Quora, Twitter, etc.)", "requires": ["00-setup-01", "00-setup-02"]},
    {"id": "02-content-03-quality-scorer", "priority": "P1", "effort": "4-6", "title": "Content: Story Quality Scorer", "requires": ["02-content-01"]},
    {"id": "02-content-04-deduplication", "priority": "P1", "effort": "2-3", "title": "Content: Story Deduplication", "requires": ["02-content-01", "02-content-02"]},
    {"id": "02-content-05-ranking", "priority": "P1", "effort": "2-3", "title": "Content: Story Ranking & Selection", "requires": ["02-content-03", "02-content-04"]},
    {"id": "02-content-06-attribution", "priority": "P1", "effort": "1-2", "title": "Content: Source Attribution System", "requires": ["02-content-01"]},
    
    # Ideas & Titles (P1)
    {"id": "03-ideas-01-reddit-adaptation", "priority": "P1", "effort": "4-5", "title": "Ideas: Adapt Reddit Stories", "requires": ["02-content-05", "01-research-01"]},
    {"id": "03-ideas-02-llm-generation", "priority": "P1", "effort": "3-4", "title": "Ideas: LLM Original Ideas", "requires": ["01-research-01"]},
    {"id": "03-ideas-03-clustering", "priority": "P1", "effort": "3-4", "title": "Ideas: Cluster into Topics", "requires": ["03-ideas-01", "03-ideas-02"]},
    {"id": "03-ideas-04-title-generation", "priority": "P1", "effort": "3-4", "title": "Ideas: Generate Titles", "requires": ["03-ideas-03"]},
    
    # Scoring (P1)
    {"id": "04-scoring-01-title-scorer", "priority": "P1", "effort": "4-5", "title": "Scoring: Title Viral Scorer", "requires": ["03-ideas-04", "01-research-01"]},
    {"id": "04-scoring-02-voice-recommendation", "priority": "P1", "effort": "2-3", "title": "Scoring: Voice Recommendation", "requires": ["04-scoring-01"]},
    {"id": "04-scoring-03-top-selection", "priority": "P1", "effort": "1-2", "title": "Scoring: Select Top 5 Titles", "requires": ["04-scoring-01"]},
    
    # Script Generation (P1)
    {"id": "05-script-01-raw-generation", "priority": "P1", "effort": "4-5", "title": "Script: Raw Generation (v0)", "requires": ["04-scoring-03", "01-research-01"]},
    {"id": "05-script-02-script-scorer", "priority": "P1", "effort": "3-4", "title": "Script: Script Viral Scorer", "requires": ["05-script-01"]},
    {"id": "05-script-03-iteration", "priority": "P1", "effort": "4-5", "title": "Script: Local Iteration (v1)", "requires": ["05-script-02", "01-research-01"]},
    {"id": "05-script-04-gpt-improvement", "priority": "P1", "effort": "3-4", "title": "Script: GPT/Local Improvement (v2+)", "requires": ["05-script-03"]},
    {"id": "05-script-05-title-improvement", "priority": "P1", "effort": "2-3", "title": "Script: Title Improvement", "requires": ["05-script-04"]},
    
    # Scene Planning (P1)
    {"id": "06-scenes-01-beat-sheet", "priority": "P1", "effort": "3-4", "title": "Scenes: Beat Sheet Generation", "requires": ["05-script-04"]},
    {"id": "06-scenes-02-shotlist", "priority": "P1", "effort": "3-4", "title": "Scenes: Shot List Creation", "requires": ["06-scenes-01"]},
    {"id": "06-scenes-03-draft-subtitles", "priority": "P1", "effort": "2-3", "title": "Scenes: Draft Subtitle Lines", "requires": ["05-script-04"]},
    
    # Audio (P1)
    {"id": "07-audio-01-tts-generation", "priority": "P1", "effort": "4-5", "title": "Audio: TTS Voiceover Generation", "requires": ["05-script-04", "04-scoring-02"]},
    {"id": "07-audio-02-normalization", "priority": "P1", "effort": "2-3", "title": "Audio: LUFS Normalization", "requires": ["07-audio-01", "01-research-03"]},
    
    # Subtitles (P1)
    {"id": "08-subtitles-01-forced-alignment", "priority": "P1", "effort": "4-5", "title": "Subtitles: Forced Alignment", "requires": ["07-audio-02", "06-scenes-03", "01-research-02"]},
    {"id": "08-subtitles-02-scene-mapping", "priority": "P1", "effort": "2-3", "title": "Subtitles: Map to Scenes", "requires": ["08-subtitles-01", "06-scenes-02"]},
    
    # Images (P1/P2)
    {"id": "09-images-01-prompt-builder", "priority": "P1", "effort": "3-4", "title": "Images: SDXL Prompt Builder", "requires": ["06-scenes-02"]},
    {"id": "09-images-02-keyframe-gen-a", "priority": "P1", "effort": "5-6", "title": "Images: Keyframe Generation Batch A", "requires": ["09-images-01", "01-research-04"]},
    {"id": "09-images-03-keyframe-gen-b", "priority": "P2", "effort": "5-6", "title": "Images: Keyframe Generation Batch B", "requires": ["09-images-02"]},
    {"id": "09-images-04-selection", "priority": "P2", "effort": "2-3", "title": "Images: Keyframe Selection", "requires": ["09-images-02", "09-images-03"]},
    
    # Video (P1/P2)
    {"id": "10-video-01-ltx-generation", "priority": "P1", "effort": "6-8", "title": "Video: LTX Clip Generation", "requires": ["09-images-04", "01-research-05"]},
    {"id": "10-video-02-interpolation", "priority": "P2", "effort": "6-8", "title": "Video: Keyframe Interpolation", "requires": ["09-images-04"]},
    {"id": "10-video-03-variant-selection", "priority": "P2", "effort": "1-2", "title": "Video: Choose Best Variant", "requires": ["10-video-01", "10-video-02"]},
    
    # Post-Production (P1/P2)
    {"id": "11-post-01-crop-resize", "priority": "P1", "effort": "2-3", "title": "Post: Crop to 9:16", "requires": ["10-video-03", "01-research-03"]},
    {"id": "11-post-02-subtitle-burn", "priority": "P1", "effort": "3-4", "title": "Post: Burn/Soft Subtitles", "requires": ["11-post-01", "08-subtitles-02"]},
    {"id": "11-post-03-bgm-sfx", "priority": "P2", "effort": "4-5", "title": "Post: Add BGM & SFX", "requires": ["11-post-02"]},
    {"id": "11-post-04-concatenation", "priority": "P1", "effort": "2-3", "title": "Post: Concatenate Shots", "requires": ["11-post-02"]},
    {"id": "11-post-05-transitions", "priority": "P2", "effort": "2-3", "title": "Post: Add Transitions", "requires": ["11-post-04"]},
    {"id": "11-post-06-color-grading", "priority": "P2", "effort": "3-4", "title": "Post: Color Grading", "requires": ["11-post-05"]},
    
    # QC & Export (P1)
    {"id": "12-qc-01-device-preview", "priority": "P1", "effort": "2-3", "title": "QC: Device Preview Testing", "requires": ["11-post-06"]},
    {"id": "12-qc-02-sync-check", "priority": "P1", "effort": "1-2", "title": "QC: Subtitle Sync Check", "requires": ["11-post-02"]},
    {"id": "12-qc-03-quality-report", "priority": "P1", "effort": "2-3", "title": "QC: Generate Quality Report", "requires": ["12-qc-01", "12-qc-02"]},
    
    # Export (P1)
    {"id": "13-export-01-final-encode", "priority": "P1", "effort": "2-3", "title": "Export: Final Video Encode", "requires": ["12-qc-03"]},
    {"id": "13-export-02-thumbnail", "priority": "P1", "effort": "1-2", "title": "Export: Generate Thumbnail", "requires": ["13-export-01"]},
    {"id": "13-export-03-metadata", "priority": "P1", "effort": "1-2", "title": "Export: Create Metadata JSON", "requires": ["13-export-01"]},
    
    # Distribution (P2)
    {"id": "14-dist-01-youtube-upload", "priority": "P2", "effort": "3-4", "title": "Distribution: YouTube Upload", "requires": ["13-export-01", "13-export-03"]},
    {"id": "14-dist-02-tiktok-upload", "priority": "P2", "effort": "3-4", "title": "Distribution: TikTok Upload", "requires": ["13-export-01", "13-export-03"]},
    {"id": "14-dist-03-instagram-upload", "priority": "P2", "effort": "3-4", "title": "Distribution: Instagram Upload", "requires": ["13-export-01", "13-export-03"]},
    {"id": "14-dist-04-facebook-upload", "priority": "P2", "effort": "3-4", "title": "Distribution: Facebook Upload", "requires": ["13-export-01", "13-export-03"]},
    
    # Analytics (P2)
    {"id": "15-analytics-01-collection", "priority": "P2", "effort": "4-5", "title": "Analytics: Data Collection", "requires": ["14-dist-01", "14-dist-02", "14-dist-03", "14-dist-04"]},
    {"id": "15-analytics-02-monetization", "priority": "P2", "effort": "3-4", "title": "Analytics: Monetization Tracking", "requires": ["15-analytics-01"]},
    {"id": "15-analytics-03-performance", "priority": "P2", "effort": "3-4", "title": "Analytics: Performance Evaluation", "requires": ["15-analytics-01"]},
    {"id": "15-analytics-04-optimization", "priority": "P2", "effort": "3-4", "title": "Analytics: Content Optimization", "requires": ["15-analytics-03"]},
]

def generate_issue(task: Dict) -> str:
    """Generate markdown content for an atomic issue."""
    requires_list = task.get("requires", [])
    requires_str = "\n".join(f"- `{req}`" for req in requires_list) if requires_list else "- None (can start immediately)"
    
    template = f"""# {task['title']}

**ID:** `{task['id']}`  
**Priority:** {task['priority']}  
**Effort:** {task['effort']} hours  
**Status:** Not Started

## Overview

[TODO: Add specific overview for this task]

## Dependencies

**Requires:**
{requires_str}

**Blocks:**
- [Tasks that depend on this one]

## Acceptance Criteria

- [ ] [Add specific acceptance criteria]
- [ ] Documentation updated
- [ ] Tests passing (if applicable)
- [ ] Code reviewed and merged

## Task Details

### Implementation

[TODO: Add implementation details, code examples, schemas]

### Testing

```bash
# Add test commands
```

## Output Files

- [List expected output files/artifacts]

## Related Files

- [List related source files or docs]

## Notes

- [Add any important notes or considerations]

## Next Steps

After completion:
- [List tasks that can proceed]
"""
    return template

def main():
    """Generate all atomic issue files."""
    base_path = Path("issues/atomic")
    base_path.mkdir(parents=True, exist_ok=True)
    
    for task in ATOMIC_TASKS:
        task_dir = base_path / task["id"]
        task_dir.mkdir(exist_ok=True)
        
        issue_file = task_dir / "issue.md"
        if not issue_file.exists():  # Don't overwrite existing
            content = generate_issue(task)
            with open(issue_file, "w") as f:
                f.write(content)
            print(f"✅ Created: {task['id']}")
        else:
            print(f"⏭️  Skipped: {task['id']} (already exists)")
    
    print(f"\n✨ Generated {len(ATOMIC_TASKS)} atomic issues!")

if __name__ == "__main__":
    main()
