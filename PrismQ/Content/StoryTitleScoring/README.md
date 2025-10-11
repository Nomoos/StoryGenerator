# StoryTitleScoring

Evaluate and score story titles for viral potential.

## Purpose

Scores titles across multiple dimensions (novelty, emotional appeal, clarity, etc.) and selects top performers.

## Modules

- **title_scoring.py**: Score titles for viral potential
  - `TitleScorer`: Multi-dimensional title evaluation

- **top_selection.py**: Select top-scoring titles
  - `TopSelector`: Filter and select best titles with diversity

## Usage

```python
from PrismQ.StoryTitleScoring.title_scoring import TitleScorer
from PrismQ.StoryTitleScoring.top_selection import TopSelector

# Score titles
scorer = TitleScorer()
scored_titles = scorer.score_all_titles(titles_by_topic)

# Select top titles
selector = TopSelector()
top_titles = selector.select_top_titles(scored_titles, top_n=5)
```
