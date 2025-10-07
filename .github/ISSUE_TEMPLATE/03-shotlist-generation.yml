---
name: "Stage 3: Shotlist Generation"
about: LLM-based scene breakdown and visual planning with Qwen2.5 or Llama-3.1
title: "[Pipeline] LLM-Based Shotlist and Scene Breakdown"
labels: ["feature", "llm", "planning", "priority: high", "stage-3"]
assignees: []
---

## 📋 Component Information

**Component**: LLM Content Enhancement  
**Stage**: 3 of 10  
**Priority**: High  
**Estimated Effort**: 2 weeks

## 🎯 Overview

Implement automatic shotlist generation from scripts, breaking down the story into visual scenes with descriptions, timing, and image generation prompts.

## 📊 Current State

- ✅ Script generation (GPT-4o-mini)
- ✅ Script revision
- ⚠️ No scene breakdown
- ⚠️ No visual planning

## ✅ Requirements

### Must Have
- [ ] Scene segmentation from script
- [ ] Visual descriptions per scene
- [ ] Duration estimation per scene
- [ ] JSON output format
- [ ] SDXL prompt generation

### Should Have
- [ ] Emotion tracking per scene
- [ ] Camera angle suggestions
- [ ] Lighting descriptions
- [ ] Movement/action notes
- [ ] Alternative LLM support (Qwen2.5, Llama-3.1)

### Nice to Have
- [ ] Storyboard visualization
- [ ] Scene transition suggestions
- [ ] Music cue recommendations

## 📝 Subtasks

### 1. Core Scene Analysis
- [ ] Implement script parser
- [ ] Create scene segmentation algorithm
- [ ] Extract scene boundaries from narration
- [ ] Calculate scene durations from timestamps

### 2. Visual Description Generation
- [ ] Design LLM prompt for scene description
- [ ] Implement visual detail extraction
- [ ] Generate camera angle suggestions
- [ ] Add emotion/mood tagging

### 3. SDXL Prompt Generation
- [ ] Create SDXL prompt templates
- [ ] Implement style consistency keywords
- [ ] Add negative prompts
- [ ] Test prompt quality with SDXL

### 4. LLM Integration
- [ ] Set up Qwen2.5-14B-Instruct
- [ ] Configure Llama-3.1-8B-Instruct (alternative)
- [ ] Implement LLM fallback logic
- [ ] Optimize inference parameters

### 5. Output Format
- [ ] Design JSON schema for shotlist
- [ ] Implement shotlist serialization
- [ ] Add validation logic
- [ ] Create example outputs

## 🎯 Performance Targets
- Scene detection accuracy: >90%
- Generation time: <5 seconds per scene
- VRAM usage: <14GB (Qwen2.5) or <8GB (Llama-3.1)

## 📁 Files to Create/Modify

**New Files:**
- `Generators/GShotlist.py`
- `schemas/shotlist_schema.json`
- `tests/test_shotlist.py`
- `examples/shotlist_example.json`

**Modified Files:**
- `requirements.txt`

## ✨ Success Criteria
- [ ] Generates shotlist from script automatically
- [ ] Scene count matches narrative flow
- [ ] Visual descriptions are detailed and cinematic
- [ ] SDXL prompts produce relevant images
- [ ] JSON output is valid and complete

## 🔗 Dependencies
- Stage 1: Environment & Model Setup
- Stage 2: ASR Enhancement (for timing alignment)

## 📚 References
- [Qwen2.5-14B-Instruct](https://huggingface.co/unsloth/Qwen2.5-14B-Instruct)
- [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
- [docs/CHILD_ISSUES.md](../docs/CHILD_ISSUES.md) - Full template details

---

**Related Documentation**: [PIPELINE.md](../PIPELINE.md) | [CHILD_ISSUES.md](../docs/CHILD_ISSUES.md)
