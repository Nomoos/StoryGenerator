# Script Development Group

**Phase:** 3 - Implementation  
**Tasks:** 5  
**Priority:** P1  
**Duration:** 2-3 days  
**Team Size:** 2-3 developers

## Overview

Generate, score, and iteratively improve scripts for selected video titles.

## Tasks

1. **05-script-01-raw-generation** (P1) - Generate raw scripts (v0)
2. **05-script-02-script-scorer** (P1) - Score scripts for quality
3. **05-script-03-iteration** (P1) - Iterate locally until plateau
4. **05-script-04-gpt-improvement** (P1) - Improve with GPT/local LLM
5. **05-script-05-title-improvement** (P1) - Generate improved title variants

## Dependencies

**Requires:** Idea Generation group (top 5 titles per segment)  
**Blocks:** Scene Planning, Audio Production

## Output Files

```
Generator/
├── scripts/
│   ├── raw_local/{gender}/{age}/v0/
│   ├── iter_local/{gender}/{age}/v1+/
│   └── gpt_improved/{gender}/{age}/v2+/
└── titles/improved/{gender}/{age}/
```
