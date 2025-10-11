# StoryTitleProcessor

Generate engaging video titles from story ideas and topics.

## Purpose

Generates multiple title variants for each topic using creative LLM prompting, optimized for short-form video platforms.

## Modules

- **title_generation.py**: Generate title variants
  - `TitleGenerator`: Creates engaging, viral-ready titles

## Usage

```python
from PrismQ.StoryTitleProcessor.title_generation import TitleGenerator

generator = TitleGenerator(llm_provider)
titles = generator.generate_titles(topic, count=10)
```
