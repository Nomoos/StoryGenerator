# Ideas: Cluster into Topics

**ID:** `03-ideas-03-clustering`  
**Priority:** P1  
**Effort:** 3-4 hours  
**Status:** ✅ Complete

## Overview

Clusters story ideas into cohesive topics/themes using LLM-based analysis. Groups similar ideas together to enable focused title generation.

## Dependencies

**Requires:**
- `03-ideas-01` - Reddit adaptation
- `03-ideas-02` - LLM generation

**Blocks:**
- `03-ideas-04` - Title generation (needs topics)

## Acceptance Criteria

- [x] TopicClusterer class implemented
- [x] Clustering algorithm working
- [x] Topics saved to JSON format
- [x] Code reviewed and merged

## Implementation

**Module:** `core/pipeline/topic_clustering.py`
**Class:** `TopicClusterer`

```python
from core.pipeline.topic_clustering import TopicClusterer

clusterer = TopicClusterer(llm_provider)
topics = clusterer.cluster_ideas(ideas, min_clusters=8, max_clusters=12)
clusterer.save_topics(topics, output_dir)
```

## Output Files

**File:** `data/topics/{gender}/{age_bucket}/topics_clustered.json`

```json
{
  "total_topics": 10,
  "clustered_at": "2024-01-01T12:00:00",
  "topics": [
    {
      "id": "topic_01",
      "name": "Relationships and Personal Connections",
      "theme": "Stories about love, friendships, and family dynamics",
      "idea_ids": ["llm_001", "reddit_abc123", "llm_005"],
      "idea_count": 3
    }
  ]
}
```

## Next Steps

- `03-ideas-04` - Generate titles for each topic
