# Step 1: Ideas → Topics → Titles (Per Segment)

**Status:** Not Started  
**Priority:** High  
**Dependencies:** Step 0 (Research Prototypes)

## Overview

Generate raw ideas, cluster them into topics, and convert topics into clickable titles for each target segment (gender/age combination).

## Target Audience
- Segments: `women/{age}` and `men/{age}`
- Age buckets: `10-13`, `14-17`, `18-23`

## Checklist

### 1.1 Ideas Generation
- [ ] Generate **≥20 raw ideas** per segment (markdown list)
- [ ] Save to: `/ideas/{segment}/{age}/YYYYMMDD_ideas.md`
- [ ] Use local LLM (Qwen2.5 or Llama3.1) for generation
- [ ] Ideas should be age-appropriate and gender-relevant

### 1.2 Topics (Clustering)
- [ ] Cluster ideas into **≥8 topics** per segment
- [ ] Save JSON to: `/topics/{segment}/{age}/YYYYMMDD_topics.json`
- [ ] Each topic should group 2-4 related ideas
- [ ] Include topic metadata (theme, keywords, potential)

### 1.3 Titles Generation
- [ ] Convert topics → **≥10 clickable titles** per segment
- [ ] Save JSON to: `/titles/{segment}/{age}/YYYYMMDD_titles.json`
- [ ] Titles should be engaging and platform-optimized
- [ ] Include title metadata (topic_id, created timestamp)

## JSON Schema Examples

### Topics JSON (`YYYYMMDD_topics.json`)
```json
{
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "topics": [
    {
      "id": "topic-001",
      "name": "Mystery and Secrets",
      "idea_ids": ["idea-001", "idea-005", "idea-012"],
      "keywords": ["mystery", "secrets", "hidden"],
      "created_utc": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### Titles JSON (`YYYYMMDD_titles.json`)
```json
{
  "segment": "women|men",
  "age_bucket": "10-13|14-17|18-23",
  "titles": [
    {
      "id": "uuid",
      "title": "The Secret That Changed Everything",
      "topic_ids": ["topic-001"],
      "created_utc": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## Acceptance Criteria

- [ ] Ideas files exist for all segment/age combinations
- [ ] At least 20 ideas per segment
- [ ] Topics JSON files exist with ≥8 topics each
- [ ] Titles JSON files exist with ≥10 titles each
- [ ] All files follow naming convention `YYYYMMDD_*.{md,json}`
- [ ] Content is age-appropriate and segment-relevant

## Related Files

- `/ideas/{segment}/{age}/` - Ideas directory
- `/topics/{segment}/{age}/` - Topics directory  
- `/titles/{segment}/{age}/` - Titles directory
- `/config/pipeline.yaml` - LLM configuration

## Microstep Validation

Use the MicrostepValidator for tracking:
- Step 2: ideas
- Step 3: topics
- Step 4: titles

Comment `@copilot check` when all artifacts are created.

## Notes

- Use consistent segment folders: `women/10-13`, `women/14-17`, `women/18-23`, `men/10-13`, `men/14-17`, `men/18-23`
- Total combinations: 6 (2 genders × 3 age buckets)
