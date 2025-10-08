# Idea Generation Group

**Phase:** 3 - Implementation  
**Tasks:** 7  
**Priority:** P1  
**Duration:** 2-3 days  
**Team Size:** 3-4 developers

## Overview

This group transforms raw content into structured video ideas, topics, and clickable titles. It includes scoring and selection of the best titles for script development.

## Tasks

1. **03-ideas-01-reddit-adaptation** (P1) - Adapt Reddit stories into video ideas
2. **03-ideas-02-llm-generation** (P1) - Generate original ideas using LLM
3. **03-ideas-03-clustering** (P1) - Cluster ideas into topics
4. **03-ideas-04-title-generation** (P1) - Generate titles from topics
5. **04-scoring-01-title-scorer** (P1) - Score titles for viral potential
6. **04-scoring-02-voice-recommendation** (P1) - Recommend voice gender (F/M)
7. **04-scoring-03-top-selection** (P1) - Select top 5 titles per segment

## Dependencies

**Requires:**
- Content Pipeline group (ranked stories)
- Phase 2: Ollama client for LLM generation

**Blocks:**
- Script Development group (needs selected titles)

## Execution Strategy

```
Day 1:
├── Dev 1: Reddit adaptation
├── Dev 2: LLM generation
└── Dev 3: Clustering

Day 2:
├── Dev 1: Title generation
├── Dev 2: Title scorer
└── Dev 3: Voice recommendation

Day 3:
└── Dev 1: Top selection (depends on scores)
```

## Success Criteria

- [ ] 20+ ideas per segment (6 segments total)
- [ ] Ideas clustered into 8+ topics per segment
- [ ] 10+ titles generated per topic
- [ ] All titles scored 0-100 with viral rubric
- [ ] Voice recommendations (F/M) for each title
- [ ] Top 5 titles selected per segment (30 total)

## Output Files

```
Generator/
├── ideas/{gender}/{age}/
│   ├── reddit_adapted.json
│   ├── llm_generated.json
│   └── all_ideas.json
├── topics/{gender}/{age}/
│   └── topics_clustered.json
├── titles/{gender}/{age}/
│   ├── titles_raw.json
│   └── titles_scored.json
└── selected/{gender}/{age}/
    └── top_5_titles.json
```

## Next Steps

After completion, the **Script Development** group can begin generating scripts for the selected titles.
