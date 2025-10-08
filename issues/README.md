# Issues Directory

This directory contains individual issue files organized by pipeline steps. Each step from the main pipeline has been broken down into separate, manageable issues.

## Directory Structure

```
issues/
├── README.md (this file)
├── INDEX.md (index of all issues)
├── step-00-research/      # Research Prototypes (Local Only)
├── step-01-ideas/         # Ideas → Topics → Titles
├── step-02-viral-score/   # Viral Score (Titles)
├── step-03-raw-script/    # Raw Script → Score → Iterate
├── step-04-improve-script/# Improve Script by GPT/Local
├── step-05-improve-title/ # Improve Title by GPT/Local
├── step-06-scene-planning/# Scene Planning
├── step-07-voiceover/     # Voiceover
├── step-08-subtitle-timing/# Subtitle Timing
├── step-09-key-images/    # Key Images per Scene (SDXL)
├── step-10-video-generation/# Video Generation
├── step-11-post-production/# Post-Production
├── step-12-quality-checks/# Quality Checks
└── step-13-final-export/  # Final Export
```

## Usage

1. Navigate to the specific step directory you want to work on
2. Read the issue file(s) in that directory
3. Follow the checklist and acceptance criteria
4. Comment `@copilot check` in the issue when you complete a task

## Related Documentation

- `/docs/MICROSTEP_VALIDATION.md` - Microstep validation system
- `/docs/GENERATOR_STRUCTURE.md` - Generator folder structure
- `/docs/PIPELINE.md` - Complete pipeline documentation
