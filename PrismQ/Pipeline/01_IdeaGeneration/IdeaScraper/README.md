# IdeaScraper

Idea generation and topic clustering for story content.

## Purpose

This subproject handles the initial stage of the content pipeline:
- Scraping and adapting ideas from external sources (e.g., Reddit)
- Generating original ideas using LLMs
- Clustering ideas into coherent topics
- Merging and organizing idea collections

## Modules

- **idea_generation.py**: Generate and adapt story ideas
  - `IdeaAdapter`: Adapt external stories to video ideas
  - `IdeaGenerator`: Generate original ideas using LLMs
  - `merge_and_save_all_ideas()`: Merge idea collections

- **topic_clustering.py**: Cluster ideas into topics
  - `TopicClusterer`: Group similar ideas into themes

## Usage

```python
from PrismQ.IdeaScraper.idea_generation import IdeaAdapter, IdeaGenerator
from PrismQ.IdeaScraper.topic_clustering import TopicClusterer
from PrismQ.Shared.interfaces.llm_provider import ILLMProvider

# Generate ideas
generator = IdeaGenerator(llm_provider)
ideas = generator.generate_ideas(gender="women", age_bucket="18-23", count=20)

# Cluster into topics
clusterer = TopicClusterer(llm_provider)
topics = clusterer.cluster_ideas(ideas)
```

## Scripts

- **scripts/generate_ideas.py**: Complete idea generation pipeline
